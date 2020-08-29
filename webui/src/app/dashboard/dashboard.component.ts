import {Component, OnDestroy, OnInit} from '@angular/core';
import {DashboardService} from '@app/dashboard/dashboard.service';

import * as moment from 'moment';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, OnDestroy {

  tiles: Array<string>;
  data: object = {};

  // options for the chart
  gradient = false;

  showXAxisLabel = false;
  xAxisLabel = 'Number';
  showYAxisLabel = false;
  yAxisLabel = 'Value';

  colorScheme = {
    domain: ['#5AA454']
  };

  // line, area
  autoScale = true;

  constructor(private dashboardService: DashboardService) {
  }

  ngOnInit(): void {
    this.dashboardService.getConfig().subscribe((config) => {
      for (const key in config.monitor) {
        this.data[key] = [{name: key, status: 'Waiting...', series: []}];
      }
      this.tiles = Object.keys(config.monitor);
    });

    this.dashboardService.$wsSubject.subscribe((data) => {
      const label = moment(data.text.timestamp).local().format('HH:mm:ss a');
      this.data[data.text.title][0].status = data.status;
      this.data[data.text.title][0].series.push({name: label, value: data.text.response_time});
      const length = this.data[data.text.title][0].series.length;
      if (length > 10) {
        this.data[data.text.title][0].series.shift();
      }
      this.data[data.text.title] = [...this.data[data.text.title]];
    });
  }

  ngOnDestroy(): void {
    this.dashboardService.$wsSubject.unsubscribe();
  }

}
