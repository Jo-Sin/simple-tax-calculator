import { Component, effect, inject } from '@angular/core';
import {MatSelectModule} from '@angular/material/select';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import {FormsModule} from '@angular/forms';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import { DataService } from './data.service';
import { AsyncPipe } from '@angular/common';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-root',
  imports: [MatInputModule, MatFormFieldModule, MatSelectModule, AsyncPipe, FormsModule, MatProgressSpinnerModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  rates$!: Observable<any>;
  private dataService = inject(DataService);
  constructor() {
    effect(() => {
      this.rates$ = this.dataService.getRates();
    });
  }

  title = 'Tax Calculator';
  selectedYear = '2025–26';
  income: number = 1;
  
  getTax(rates: any) {
    let yearRates = rates.find((x: any) => x.year == this.selectedYear);
    let centTax = 0;
    if (yearRates.rates[0].threshold >= this.income)
      return 0;
    for (let index in yearRates.rates) {
      let i = Number(index);
      if (i === 0)
        continue;
      let item = yearRates.rates[i];
      let prevItem = yearRates.rates[i - 1];
      let gap = (item.threshold == -1 || this.income < item.threshold ? this.income : item.threshold) - prevItem.threshold;
      centTax += gap * item.rate;
      if (this.income < item.threshold)
        break;
    }
    return (centTax/100).toFixed(2);
  }
}
