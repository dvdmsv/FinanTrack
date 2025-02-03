import { Component } from '@angular/core';
import { Categoria, Presupuesto } from '../../interfaces/responses';
import { CurrencyPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import Swal from 'sweetalert2';
import { ComunicacionInternaService } from '../../servicios/comunicacion-interna.service';
import { FinanzasPresupuestosService } from '../../servicios/finanzas-servicios/finanzas-presupuestos.service';
import { FinanzasCategoriasService } from '../../servicios/finanzas-servicios/finanzas-categorias.service';

@Component({
  selector: 'app-presupuestos',
  imports: [CurrencyPipe, FormsModule],
  templateUrl: './presupuestos.component.html',
  styleUrl: './presupuestos.component.css'
})
export class PresupuestosComponent {
  constructor(private finanzasCategoriasService: FinanzasCategoriasService, private finanzasPresupuestosService: FinanzasPresupuestosService, private comunicacionInternaService: ComunicacionInternaService) {}

  presupuestos: Presupuesto[] = [];
  categorias: Categoria[] = [];

  categoria: string = '';
  porcentaje: number = 0;

  ngOnInit() {
    this.getPresupuestos();
    this.getCategorias();
    this.refrescarValores();
  }

  getPresupuestos() {
    this.finanzasPresupuestosService.getPresupuestos().subscribe({
      next: data => {
        this.presupuestos = data.presupuestos;
      }
    });
  }

  getCategorias() {
    this.finanzasCategoriasService.getCategorias().subscribe({
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
    this.finanzasPresupuestosService.deletePresupuesto(id).subscribe(()=>{
      this.getPresupuestos();
    });
    
  }

  setPresupuesto() {
    this.finanzasPresupuestosService.setPresupuesto(this.categoria, this.porcentaje)
    .subscribe({
        next: (data) => {
          Swal.fire({
            position: 'top',
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

  private refrescarValores() {
    this.comunicacionInternaService.refreshData.subscribe(data => {
      if(data == true){
        this.getPresupuestos();
      }
    });
  }

}
