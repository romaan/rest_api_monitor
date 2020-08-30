import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {environment} from '../../environments/environment';
import {webSocket, WebSocketSubject} from 'rxjs/webSocket';

declare let window;

@Injectable({
  providedIn: 'root'
})
export class MonitorService {

  private httpUrl = `${environment.url}`;
  public $wsSubject: WebSocketSubject<any>;

  constructor(private http: HttpClient) {
    if (environment.production) {
      this.httpUrl = `${window.location.host}:${window.location.port}`;
    } else {
      this.httpUrl = environment.url;
    }
    this.$wsSubject = webSocket(`ws://${this.httpUrl}/health-record`);
  }

  public getConfig(): Promise<any> {
    return this.http.get(`http://${this.httpUrl}/api/config`).toPromise();
  }

  public getData(service: string): Promise<any> {
    return this.http.get(`http://${this.httpUrl}/api/health/${service}?ordering=timestamp`).toPromise();
  }
}
