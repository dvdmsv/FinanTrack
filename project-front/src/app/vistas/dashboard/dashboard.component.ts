import { Component, OnInit } from '@angular/core';
import { RegistroPorCategoria } from '../../interfaces/responses';
import { CurrencyPipe, NgFor } from '@angular/common';
import { ComunicacionInternaService } from '../../servicios/comunicacion-interna.service';
import { DonutComponent } from '../graficos/donut/donut.component';
import { FinanzasSaldoService } from '../../servicios/finanzas-servicios/finanzas-saldo.service';
import { FinanzasRegistrosService } from '../../servicios/finanzas-servicios/finanzas-registros.service';

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

  constructor(private finanzasRegistrosService: FinanzasRegistrosService,private finanzasSaldoService: FinanzasSaldoService, private comunicacionInternaService: ComunicacionInternaService) {}

  ngOnInit(): void {
    this.cargarSaldo();
    this.cargarRegistrosPorCategoria();
    this.refrescarValores();
  }

  private cargarSaldo(): void {
    this.finanzasSaldoService.getSaldo().subscribe({
      next: (data) => {
        this.saldo = data.saldo;
      },
      error: (err) => {
        console.error('Error al obtener el saldo:', err);
      }
    });
  }

  private cargarRegistrosPorCategoria(): void {
    this.finanzasRegistrosService.getRegistrosPorCategoria().subscribe({
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
