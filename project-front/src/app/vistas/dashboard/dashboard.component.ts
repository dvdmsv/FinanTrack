import { Component, OnInit } from '@angular/core';
import { FinanzasService } from '../../servicios/finanzas.service';
import { RegistroPorCategoria } from '../../interfaces/responses';
import { CurrencyPipe, NgFor } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  imports: [CurrencyPipe],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  saldo: number = 0;
  registrosPorCategoria: RegistroPorCategoria[] = [];
  username = localStorage.getItem('username');

  constructor(private finanzasService: FinanzasService) {}

  ngOnInit(): void {
    this.cargarSaldo();
    this.cargarRegistrosPorCategoria();
  }

  private cargarSaldo(): void {
    this.finanzasService.getSaldo().subscribe({
      next: (data) => {
        this.saldo = data.saldo;
      },
      error: (err) => {
        console.error('Error al obtener el saldo:', err);
      }
    });
  }

  private cargarRegistrosPorCategoria(): void {
    this.finanzasService.getRegistrosPorCategoria().subscribe({
      next: (data) => {
        this.registrosPorCategoria = data.categorias;
      },
      error: (err) => {
        console.error('Error al obtener registros por categoría:', err);
      }
    });
  }
}
