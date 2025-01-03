import { Component } from '@angular/core';
import { FinanzasService } from '../../servicios/finanzas.service';
import { Registro } from '../../interfaces/responses';
import { CurrencyPipe } from '@angular/common';

@Component({
  selector: 'app-registros',
  imports: [CurrencyPipe],
  templateUrl: './registros.component.html',
  styleUrl: './registros.component.css'
})
export class RegistrosComponent {
  constructor(private finanzasService: FinanzasService) {}

  registros: Registro[] = [];

  ngOnInit() {
    this.getRegistrosUser();
  }

  getRegistrosUser() {
    this.finanzasService.getRegistrosUser().subscribe({
      next: data => {
        this.registros = data.registros;
      }
    })
  }
}
