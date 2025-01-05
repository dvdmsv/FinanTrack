import { Component } from '@angular/core';
import { FinanzasService } from '../../../servicios/finanzas.service';
import { Categoria, Registro } from '../../../interfaces/responses';
import {  FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import Swal from 'sweetalert2';
import { Router } from '@angular/router';

@Component({
  selector: 'app-registro-nuevo',
  imports: [FormsModule],
  templateUrl: './registro-nuevo.component.html',
  styleUrl: './registro-nuevo.component.css',
})
export class RegistroNuevoComponent {
  constructor(private finanzasService: FinanzasService, private router: Router) {}

  categorias: Categoria[] = [];

  
  categoria: string = '';
  tipo: string = '';
  cantidad: number = 0;
  concepto: string = '';
  

  ngOnInit() {
    this.getCategorias();
  }

  getCategorias() {
    this.finanzasService.getCategorias().subscribe({
      next: (data) => {
        this.categorias = [...data.categoriasGlobales, ...data.categoriasUnicas];
      },
      error: (err) => {
        console.error('Error al obtener categorías:', err);
      },
    });
  }

  generarRegistro(): void {
    if (!this.categoria || !this.tipo || !this.concepto || this.cantidad == 0) {
      console.warn('El formulario no está completo');
      return;
    }
    this.finanzasService.generarRegistro(this.categoria, this.tipo, this.cantidad, this.concepto).subscribe({
      next: data => {
        Swal.fire({
            position: 'top-end',
            icon: 'success',
            title: 'Registrado correctamente',
            showConfirmButton: false,
            timer: 1500,
            toast: true
          });
        this.categoria = "";
        this.cantidad = 0;
        this.concepto = "";
        this.tipo = "";
      }
    });
  }
}
