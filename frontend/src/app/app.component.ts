import { Component, effect, inject } from '@angular/core';
import {MatSelectModule} from '@angular/material/select';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {FormsModule} from '@angular/forms';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatTableModule} from '@angular/material/table';
import { DataService, TaxRate } from './data.service';
import { AsyncPipe } from '@angular/common';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-root',
  imports: [MatInputModule, MatFormFieldModule, MatSelectModule, AsyncPipe, FormsModule, MatProgressSpinnerModule, MatTableModule],
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
  dataSource: any[] = [];
  income: number = 1;
  
  calculateTax(rates: TaxRate[]) {
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

  updateTable(rates: TaxRate[]) {
    let yearRates = rates.find((x: any) => x.year == this.selectedYear);
    this.dataSource = [];
    if (yearRates) {
      for (let item of yearRates?.brackets) {
        this.dataSource.push({
          taxBracket: `$${item.min} ${item.max == -1 ? 'and over' : `- $${item.max}`}`,
          taxable: item.rate == 0 ? 'Nil' : `${item.base > 0 ? `$${item.base} plus ` : ''}${item.rate}c per $1 above $${item.min - 1}`
        })
      }
    }
    
    return;
  }
}
