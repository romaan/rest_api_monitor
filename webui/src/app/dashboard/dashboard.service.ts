import { Injectable } from '@angular/core';
import {HttpClient, HttpResponse} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  url = `/api/config`;

  constructor(private http: HttpClient) { }

  public getConfig(): Observable<any> {
    return this.http.get(this.url);
  }
}
