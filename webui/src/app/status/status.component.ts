import {Component, OnInit} from '@angular/core';
import {MonitorService} from '@app/shared/monitor.service';
import * as moment from 'moment';
import {Subscription} from 'rxjs';

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.scss']
})
export class StatusComponent implements OnInit {

  data = [];
  indexMap = {};
  monitorSubscription: Subscription = null;

  constructor(private monitorService: MonitorService) {
  }

  ngOnInit(): void {

    this.monitorService.getConfig().then((config) => {
      for (const key in config.monitor) {
        if (config.monitor.hasOwnProperty(key)) {
          this.indexMap[key] = this.data.length;
          this.data.push({text: key, cols: 1, rows: 1, color: 'lightyellow'});
        }
      }
    });

    if (this.monitorSubscription === null) {
      this.monitorSubscription = this.monitorService.$wsSubject.subscribe((data) => {
        const label = moment(data.text.timestamp).local().format('HH:mm:ss a');
        const index = this.indexMap[data.text.title];
        this.data[index].lastUpdate = label;
        if (data.status === 'Up') {
          this.data[index].color = 'lightgreen';
        } else if (data.status === 'Down') {
          this.data[index].color = 'tomato';
        }
      });
    }
  }

}
