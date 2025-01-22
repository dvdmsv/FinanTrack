import { Component } from '@angular/core';
import { FinanzasService } from '../../servicios/finanzas.service';
import { Categoria, Presupuesto } from '../../interfaces/responses';
import { CurrencyPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-presupuestos',
  imports: [CurrencyPipe, FormsModule],
  templateUrl: './presupuestos.component.html',
  styleUrl: './presupuestos.component.css'
})
export class PresupuestosComponent {
  constructor(private finanzasService: FinanzasService) {}

  presupuestos: Presupuesto[] = [];
  categorias: Categoria[] = [];

  categoria: string = '';
  porcentaje: number = 0;

  ngOnInit() {
    this.getPresupuestos();
    this.getCategorias();
  }

  getPresupuestos() {
    this.finanzasService.getPresupuestos().subscribe({
      next: data => {
        this.presupuestos = data.presupuestos;
        console.log(this.presupuestos);
      }
    });
  }

  getCategorias() {
    this.finanzasService.getCategorias().subscribe({
      next: (data) => {
        this.categorias = [
          ...data.categoriasGlobales,
          ...data.categoriasUnicas,
        ];
      },
      error: (err) => {
        console.error('Error al obtener categorías:', err);
      },
    });
  }

  eliminar(id: number){
    this.finanzasService.deletePresupuesto(id).subscribe(()=>{
      this.getPresupuestos();
    });
    
  }

  setPresupuesto() {
    this.finanzasService.setPresupuesto(this.categoria, this.porcentaje)
    .subscribe({
        next: (data) => {
          Swal.fire({
            position: 'top-end',
            icon: 'success',
            title: 'Registrado correctamente',
            showConfirmButton: false,
            timer: 1500,
            toast: true,
          });
          this.categoria = '';
          this.porcentaje = 0;
          this.getPresupuestos();
        },
      });
  }

}
