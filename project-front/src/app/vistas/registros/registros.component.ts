import { Component } from '@angular/core';
import { FinanzasService } from '../../servicios/finanzas.service';
import { Categoria, Registro } from '../../interfaces/responses';
import { CurrencyPipe } from '@angular/common';
import Swal from 'sweetalert2';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-registros',
  imports: [CurrencyPipe, FormsModule],
  templateUrl: './registros.component.html',
  styleUrl: './registros.component.css',
})
export class RegistrosComponent {
  constructor(private finanzasService: FinanzasService) {}

  registros: Registro[] = [];
  categorias: Categoria[] = [];

  categoria: string = '';
  tipo: string = '';
  cantidad: number = 0;
  concepto: string = '';

  ngOnInit() {
    this.getRegistrosUser();
    this.getCategorias();
  }

  getRegistrosUser() {
    this.finanzasService.getRegistrosUser().subscribe({
      next: (data) => {
        this.registros = data.registros;
      },
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

  eliminar(id: number) {
    this.finanzasService.deleteRegistro(id).subscribe(()=>{
      this.getRegistrosUser();
    });
  }

  generarRegistro(): void {
    if (!this.categoria || !this.tipo || !this.concepto || this.cantidad == 0) {
      console.warn('El formulario no está completo');
      return;
    }
    this.finanzasService
      .generarRegistro(this.categoria, this.tipo, this.cantidad, this.concepto)
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
          this.cantidad = 0;
          this.concepto = '';
          this.tipo = '';
          this.getRegistrosUser();
        },
        error: (err) => {
          Swal.fire({
            position: 'top-end',
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
