import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatCardModule} from '@angular/material/card';
import {HttpClientModule} from '@angular/common/http';
import {MatIconModule} from '@angular/material/icon';
import {MonitorService} from './monitor.service';


@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    MatToolbarModule,
    MatGridListModule,
    MatCardModule,
    MatIconModule,
    HttpClientModule,
  ],
  exports: [
    MatToolbarModule,
    MatGridListModule,
    MatCardModule,
    MatIconModule
  ],
  providers: [
    MonitorService
  ]
})
export class SharedModule { }
