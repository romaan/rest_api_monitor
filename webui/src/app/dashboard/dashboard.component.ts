import {Component, OnInit} from '@angular/core';
import {DashboardService} from "@app/dashboard/dashboard.service";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  tiles = [
    {text: 'One', cols: 1, rows: 1, color: '#142A5C'},
    {text: 'Two', cols: 1, rows: 1, color: '#B7A0E8'},
    {text: 'Three', cols: 1, rows: 1, color: '#FF0000'},
    {text: 'One', cols: 1, rows: 1, color: '#142A5C'},
    {text: 'Two', cols: 1, rows: 1, color: '#B7A0E8'},
    {text: 'Three', cols: 1, rows: 1, color: '#FF0000'},
    {text: 'One', cols: 1, rows: 1, color: '#142A5C'},
    {text: 'Two', cols: 1, rows: 1, color: '#B7A0E8'},
    {text: 'Three', cols: 1, rows: 1, color: '#FF0000'},
  ];

  public multi = [
    {
      "name": "Germany",
      "series": [
        {
          "name": "2010",
          "value": 730
        },
        {
          "name": "2011",
          "value": 894
        },
        {
          "name": "2012",
          "value": 730
        },
        {
          "name": "2013",
          "value": 100
        },
        {
          "name": "2014",
          "value": 1000
        },
        {
          "name": "2015",
          "value": 5
        }
      ]
    }
  ];

  // options for the chart
  showXAxis = true;
  showYAxis = true;
  gradient = false;
  showLegend = false;
  showXAxisLabel = false;
  xAxisLabel = 'Number';
  showYAxisLabel = false;
  yAxisLabel = 'Value';
  timeline = true;

  colorScheme = {
    domain: ['#5AA454']
  };

  // line, area
  autoScale = true;

  constructor(dashboardService: DashboardService) {
  }

  ngOnInit(): void {
  }

}
