import { Component, effect, inject } from '@angular/core';
import {MatSelectModule} from '@angular/material/select';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {FormsModule} from '@angular/forms';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import { DataService, TaxRate } from './data.service';
import { AsyncPipe } from '@angular/common';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-root',
  imports: [MatInputModule, MatFormFieldModule, MatSelectModule, AsyncPipe, FormsModule, MatProgressSpinnerModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  rates$!: Observable<TaxRate[]>;
  private dataService = inject(DataService);
  constructor() {
    effect(() => {
      this.rates$ = this.dataService.getRates();
    });
  }

  title = 'Tax Calculator';
  selectedYear = '2025–26';
  income: number = 1;
  
  getTax(rates: TaxRate[]) {
    let yearRates = rates.find((x: any) => x.year == this.selectedYear);
    let centTax = 0;
    if (yearRates) {
      for (let item of yearRates?.brackets) {
        if ((item.max === -1) || ((item.min <= this.income) && (this.income <= item.max))) {
          centTax = Math.round(item.base * 100 + (this.income - item.min + 1) * item.rate);
          break;
        }
      }
    }
    return (centTax/100).toFixed(2);
  }
}
