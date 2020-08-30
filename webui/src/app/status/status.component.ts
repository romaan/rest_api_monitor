import {AfterViewInit, Component, OnDestroy} from '@angular/core';
import {MonitorService} from '@app/shared/monitor.service';
import * as moment from 'moment';

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.scss']
})
export class StatusComponent implements AfterViewInit, OnDestroy {

  data = [];
  indexMap = {};

  constructor(private monitorService: MonitorService) {
  }

  ngAfterViewInit(): void {
    this.monitorService.getConfig().subscribe((config) => {
      for (const key in config.monitor) {
        this.indexMap[key] = this.data.length;
        this.data.push({text: key, cols: 1, rows: 1, color: 'lightyellow'});
      }
    });

    this.monitorService.$wsSubject.subscribe((data) => {
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

  ngOnDestroy(): void {
    this.monitorService.$wsSubject.unsubscribe();
  }
}
