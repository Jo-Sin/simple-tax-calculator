import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

interface TaxBracket {
  base: number;
  min: number;
  max: number;
  rate: number;
}

export interface TaxRate {
  year: string;
  brackets: TaxBracket[];
}

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private taxRatesUrl = 'http://localhost:5000/api/rates';
  private http = inject(HttpClient);

  getRates(): Observable<TaxRate[]> {
    return this.http.get<TaxRate[]>(this.taxRatesUrl);
  }
}
