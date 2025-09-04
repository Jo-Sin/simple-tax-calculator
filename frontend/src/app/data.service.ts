import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private taxRatesUrl = 'http://localhost:5000/api/rates';
  private http = inject(HttpClient);

  getRates(): Observable<any> {
    return this.http.get<any>(this.taxRatesUrl);
  }
}
