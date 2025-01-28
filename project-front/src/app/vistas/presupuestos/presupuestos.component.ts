import { Component } from '@angular/core';
import { FinanzasService } from '../../servicios/finanzas.service';
import { Categoria, Presupuesto } from '../../interfaces/responses';
import { CurrencyPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import Swal from 'sweetalert2';
import { ComunicacionInternaService } from '../../servicios/comunicacion-interna.service';

@Component({
  selector: 'app-presupuestos',
  imports: [CurrencyPipe, FormsModule],
  templateUrl: './presupuestos.component.html',
  styleUrl: './presupuestos.component.css'
})
export class PresupuestosComponent {
  constructor(private finanzasService: FinanzasService, private comunicacionInternaService: ComunicacionInternaService) {}

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
    this.finanzasService.getPresupuestos().subscribe({
      next: data => {
        this.presupuestos = data.presupuestos;
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
