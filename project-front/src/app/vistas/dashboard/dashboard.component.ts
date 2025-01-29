import { Component, OnInit } from '@angular/core';
import { FinanzasService } from '../../servicios/finanzas.service';
import { RegistroPorCategoria } from '../../interfaces/responses';
import { CurrencyPipe, NgFor } from '@angular/common';
import { ComunicacionInternaService } from '../../servicios/comunicacion-interna.service';
import { DonutComponent } from '../graficos/donut/donut.component';

@Component({
  selector: 'app-dashboard',
  imports: [CurrencyPipe, DonutComponent],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  saldo: number = 0;
  registrosPorCategoria: RegistroPorCategoria[] = [];
  username = localStorage.getItem('username');
  gastoTotal: number = 0;

  constructor(private finanzasService: FinanzasService, private comunicacionInternaService: ComunicacionInternaService) {}

  ngOnInit(): void {
    this.cargarSaldo();
    this.cargarRegistrosPorCategoria();
    this.refrescarValores();
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

        // Obtener el gasto total de todas las categorías
        this.gastoTotal = 0;
        this.registrosPorCategoria.forEach(registro => {
          this.gastoTotal += registro.total_cantidad;
        });
        
      },
      error: (err) => {
        console.error('Error al obtener registros por categoría:', err);
      }
    });
  }

  private refrescarValores() {
    this.comunicacionInternaService.refreshData.subscribe(data => {
      if(data == true){
        this.cargarSaldo();
        this.cargarRegistrosPorCategoria();
      }
    });
  }
}
