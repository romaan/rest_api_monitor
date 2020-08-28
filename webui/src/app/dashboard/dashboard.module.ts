import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './dashboard.component';
import {RouterModule, Routes} from '@angular/router';
import {NgxChartsModule} from '@swimlane/ngx-charts';
import {SharedModule} from '../shared/shared.module';
import {DashboardService} from './dashboard.service';


const routes: Routes = [
  {
    path: '',
    component: DashboardComponent
  }
];

@NgModule({
  declarations: [
    DashboardComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    NgxChartsModule,
    RouterModule.forChild(routes)
  ],
  providers: [
    DashboardService
  ]
})
export class DashboardModule { }
