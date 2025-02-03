import { Component } from '@angular/core';
import { Categoria, Registro } from '../../interfaces/responses';
import { CurrencyPipe } from '@angular/common';
import Swal from 'sweetalert2';
import { FormsModule } from '@angular/forms';
import { ComunicacionInternaService } from '../../servicios/comunicacion-interna.service';
import { FinanzasRegistrosService } from '../../servicios/finanzas-servicios/finanzas-registros.service';
import { FinanzasCategoriasService } from '../../servicios/finanzas-servicios/finanzas-categorias.service';

@Component({
  selector: 'app-registros',
  imports: [CurrencyPipe, FormsModule],
  templateUrl: './registros.component.html',
  styleUrl: './registros.component.css',
})
export class RegistrosComponent {
  constructor(private finanzasCategoriasService: FinanzasCategoriasService, private finanzasRegistrosService: FinanzasRegistrosService, private comunicacionInternaService: ComunicacionInternaService) {}

  registros: Registro[] = [];
  categorias: Categoria[] = [];

  categoria: string = '';
  tipo: string = '';
  cantidad: number = 0;
  concepto: string = '';

  meses = [
    { nombre: "Enero", valor: 1 },
    { nombre: "Febrero", valor: 2 },
    { nombre: "Marzo", valor: 3 },
    { nombre: "Abril", valor: 4 },
    { nombre: "Mayo", valor: 5 },
    { nombre: "Junio", valor: 6 },
    { nombre: "Julio", valor: 7 },
    { nombre: "Agosto", valor: 8 },
    { nombre: "Septiembre", valor: 9 },
    { nombre: "Octubre", valor: 10 },
    { nombre: "Noviembre", valor: 11 },
    { nombre: "Diciembre", valor: 12 }
  ];

  mesSeleccionado: number = 0

  ngOnInit() {
    this.getRegistrosUser();
    this.getCategorias();
  }

  getRegistrosPorMes() {
    if(this.mesSeleccionado == 0){
      this.getRegistrosUser();
    }
    this.finanzasRegistrosService.getRegistrosPorMes(this.mesSeleccionado).subscribe({
      next: (data) => {
        this.registros = data.registros;
      }
    })
  }

  getRegistrosUser() {
    this.finanzasRegistrosService.getRegistrosUser().subscribe({
      next: (data) => {
        this.registros = data.registros;
      },
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

  eliminar(id: number) {
    this.finanzasRegistrosService.deleteRegistro(id).subscribe(()=>{
      this.getRegistrosUser();
      this.comunicacionInternaService.setRefreshData();
    });
  }

  generarRegistro(): void {
    if (!this.categoria || !this.tipo || !this.concepto || this.cantidad == 0) {
      console.warn('El formulario no está completo');
      return;
    }
    this.finanzasRegistrosService
      .generarRegistro(this.categoria, this.tipo, this.cantidad, this.concepto)
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
          this.cantidad = 0;
          this.concepto = '';
          this.tipo = '';
          this.getRegistrosUser();
          this.comunicacionInternaService.setRefreshData();
        },
        error: (err) => {
          Swal.fire({
            position: 'top',
            icon: 'error',
            title: err.error.error,
            showConfirmButton: false,
            timer: 1500,
            toast: true,
          });
        }

      });
  }
}
