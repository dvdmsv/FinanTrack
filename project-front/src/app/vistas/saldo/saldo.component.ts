import { Component } from '@angular/core';
import { FinanzasService } from '../../servicios/finanzas.service';
import { FormsModule } from '@angular/forms';
import Swal from 'sweetalert2';
import { GetPresupuestosResponse, Presupuesto } from '../../interfaces/responses';

@Component({
  selector: 'app-saldo',
  imports: [FormsModule],
  templateUrl: './saldo.component.html',
  styleUrl: './saldo.component.css'
})
export class SaldoComponent {
  constructor(private finanzasService:  FinanzasService) {}

  saldo: number = 0;
  nuevoSaldo: number = 0;
  editar: boolean = false;
  presupuestos: Presupuesto[] = [];

  ngOnInit() {
    this.cargarSaldo();
    this.getPresupuestos()
  }

  cargarSaldo(): void {
    this.finanzasService.getSaldo().subscribe({
      next: (data) => {
        this.saldo = data.saldo;
        this.nuevoSaldo = this.saldo;
      },
      error: (err) => {
        console.error('Error al obtener el saldo:', err);
      }
    });
  }

  setSaldo() {
    // Se actualiza el saldo del usuario
    this.finanzasService.setSaldo(this.nuevoSaldo).subscribe({
      next: () =>{
        Swal.fire({
            position: 'top',
            icon: 'success',
            title: 'Saldo actualizado',
            showConfirmButton: false,
            timer: 1500,
            toast: true
        });
        // Se actualizan todos los presupuestos en base al saldo del usuario
        this.presupuestos.forEach(presupuesto => {
          this.finanzasService.setPresupuesto(presupuesto.categoria, presupuesto.porcentaje).subscribe();
        });
        // Se vuelve a cargar el saldo
        this.cargarSaldo();
      }
    });
  }

  getPresupuestos() {
    this.finanzasService.getPresupuestos().subscribe({
      next: data => {
        this.presupuestos = data.presupuestos;
        console.log(this.presupuestos);
      }
    });
  }

  setEditar() {
    this.editar = !this.editar
  }

}
