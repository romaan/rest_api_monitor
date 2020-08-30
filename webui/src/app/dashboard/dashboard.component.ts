import {Component, OnInit} from '@angular/core';
import {MonitorService} from '@app/shared/monitor.service';

import * as moment from 'moment';
import {LineModel} from '@app/dashboard/dashboard.model';
import {Subscription} from 'rxjs';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  indexMap = {};
  data: LineModel[] = [];
  monitorSubscription: Subscription = null;
  show = false;

  // options for the chart

  colorScheme = {
    domain: []
  };

  // line, area
  autoScale = true;

  constructor(private monitorService: MonitorService) {
  }

  ngOnInit(): void {
    const that = this;
    this.show = false;
    this.monitorService.getConfig().then((config) => {
      for (const key in config.monitor) {
        if (config.monitor.hasOwnProperty(key)) {
          this.indexMap[key] = this.data.length;
          this.data.push({name: key, series: []});
          this.colorScheme.domain.push(that.getRandomColor());
        }
      }
      this.show = true;
    });

    if (this.monitorSubscription === null) {
      this.monitorSubscription = this.monitorService.$wsSubject.subscribe((data) => {
        const label = moment(data.text.timestamp).local().format('HH:mm:ss a');
        const index = this.indexMap[data.text.title];
        this.data[index].status = data.status;

        this.data[index].series.push({name: label, value: data.text.response_time});
        const length = this.data[index].series.length;
        if (length > 100) {
          this.data[index].series.shift();
        }
        this.data = [...this.data];
      });
    }
  }

  private getRandomColor(): string {
    let letters = '0123456789'.split('');
    let color = '#';
    color += letters[Math.round(Math.random() * 9)];
    letters = '0123456789ABCDEF'.split('');
    for (let i = 0; i < 5; i++) {
      color += letters[Math.round(Math.random() * 15)];
    }
    return color;
  }
}
