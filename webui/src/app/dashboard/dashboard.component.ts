import {AfterViewInit, Component, OnDestroy} from '@angular/core';
import {MonitorService} from '@app/shared/monitor.service';

import * as moment from 'moment';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements AfterViewInit, OnDestroy {

  indexMap = {};
  data = [];

  // options for the chart
  gradient = false;

  showXAxisLabel = false;
  xAxisLabel = 'Number';
  showYAxisLabel = false;
  yAxisLabel = 'Value';

  colorScheme = {
    domain: []
  };

  // line, area
  autoScale = true;

  constructor(private monitorService: MonitorService) {
  }

  ngAfterViewInit(): void {
    let that = this;
    this.monitorService.getConfig().subscribe((config) => {
      for (const key in config.monitor) {
        this.indexMap[key] = this.data.length;
        this.data.push({name: key, series: []});
        this.colorScheme.domain.push(that.getRandomColor());
      }
    });

    this.monitorService.$wsSubject.subscribe((data) => {
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

  ngOnDestroy(): void {
    this.monitorService.$wsSubject.unsubscribe();
  }

  getRandomColor(): any {
    let letters = '0123456789'.split('');
    let color = '#';
    color += letters[Math.round(Math.random() * 9)];
    letters = '0123456789ABCDEF'.split('');
    for (var i = 0; i < 5; i++) {
      color += letters[Math.round(Math.random() * 15)];
    }
    return color;
  }
}
