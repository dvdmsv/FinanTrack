import { Component } from '@angular/core';
import { DashboardComponent } from "../dashboard/dashboard.component";
import { RegistrosComponent } from "../registros/registros.component";
import { PresupuestosComponent } from "../presupuestos/presupuestos.component";
import { ComunicacionInternaService } from '../../servicios/comunicacion-interna.service';
import { CurrencyPipe } from '@angular/common';
import { FinanzasSaldoService } from '../../servicios/finanzas-servicios/finanzas-saldo.service';

@Component({
  selector: 'app-test-dashboard',
  imports: [DashboardComponent, RegistrosComponent, PresupuestosComponent, CurrencyPipe],
  templateUrl: './test-dashboard.component.html',
  styleUrl: './test-dashboard.component.css'
})
export class TestDashboardComponent {

  saldo: number = 0;
  username = localStorage.getItem('username');

  constructor(private finanzasSaldoService: FinanzasSaldoService, private comunicacionInternaService: ComunicacionInternaService) {}

  ngOnInit(): void {
    this.cargarSaldo();
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

  private refrescarValores() {
    this.comunicacionInternaService.refreshData.subscribe(data => {
      if(data == true){
        this.cargarSaldo();
      }
    });
  }
}
