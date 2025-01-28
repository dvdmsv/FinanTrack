import { Component, NgModule } from '@angular/core';
import { FinanzasService } from '../../servicios/finanzas.service';
import { Categoria } from '../../interfaces/responses';
import { FormsModule } from '@angular/forms';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-categorias-personales',
  imports: [FormsModule],
  templateUrl: './categorias-personales.component.html',
  styleUrl: './categorias-personales.component.css'
})
export class CategoriasPersonalesComponent {
  constructor(private finanzasService: FinanzasService) {}

  categoriasUnicas: Categoria[] = [];
  nombreCategoria: string = "";

  ngOnInit() {
    this.cargarCategorias();
  }

  cargarCategorias() {
    this.finanzasService.getCategoriasUnicas().subscribe({
      next: (data) => {
        this.categoriasUnicas = data.categoriasUnicas;
      },
      error: (err) => {
        console.error('Error al obtener las categorias:', err);
      }
    });
  }

  eliminar(id: number) {
    this.finanzasService.deleteCategoria(id).subscribe(()=>{
      this.cargarCategorias();
    })
  }

  setCategoria() {
    this.finanzasService.setCategoria(this.nombreCategoria, false).subscribe({
      next: () =>{
        this.cargarCategorias();
        Swal.fire({
            position: 'top',
            icon: 'success',
            title: 'Categoria creada',
            showConfirmButton: false,
            timer: 1500,
            toast: true,
          });
        this.nombreCategoria = "";
      },
      error: (err) => {
        Swal.fire({
            position: 'top',
            icon: 'error',
            title: err.error['messaje'],
            showConfirmButton: false,
            timer: 1500,
            toast: true,
          });
      }
    });
  }
}
