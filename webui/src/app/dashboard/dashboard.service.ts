import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable, Subscription} from 'rxjs';
import {environment} from '../../environments/environment';
import {webSocket, WebSocketSubject} from 'rxjs/webSocket';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  private httpUrl = `http://${environment.url}`;
  public $wsSubject: WebSocketSubject<any>;

  constructor(private http: HttpClient) {
    this.$wsSubject = webSocket(`ws://${environment.url}/health-record`);
  }

  public getConfig(): Observable<any> {
    return this.http.get(`${this.httpUrl}/api/config`);
  }
}
