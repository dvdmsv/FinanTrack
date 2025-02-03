import { Component, NgModule } from '@angular/core';
import { Categoria } from '../../interfaces/responses';
import { FormsModule } from '@angular/forms';
import Swal from 'sweetalert2';
import { FinanzasCategoriasService } from '../../servicios/finanzas-servicios/finanzas-categorias.service';

@Component({
  selector: 'app-categorias-personales',
  imports: [FormsModule],
  templateUrl: './categorias-personales.component.html',
  styleUrl: './categorias-personales.component.css'
})
export class CategoriasPersonalesComponent {
  constructor(private finanzasCategoriasService: FinanzasCategoriasService) {}

  categoriasUnicas: Categoria[] = [];
  nombreCategoria: string = "";

  ngOnInit() {
    this.cargarCategorias();
  }

  cargarCategorias() {
    this.finanzasCategoriasService.getCategoriasUnicas().subscribe({
      next: (data) => {
        this.categoriasUnicas = data.categoriasUnicas;
      },
      error: (err) => {
        console.error('Error al obtener las categorias:', err);
      }
    });
  }

  eliminar(id: number) {
    this.finanzasCategoriasService.deleteCategoria(id).subscribe(()=>{
      this.cargarCategorias();
    })
  }

  setCategoria() {
    this.finanzasCategoriasService.setCategoria(this.nombreCategoria, false).subscribe({
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
