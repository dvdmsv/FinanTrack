import { Component } from '@angular/core';
import {
  AnioRegistro,
  Categoria,
  MesRegistro,
  Registro,
} from '../../interfaces/responses';
import { CurrencyPipe, NgFor } from '@angular/common';
import Swal from 'sweetalert2';
import { FormsModule } from '@angular/forms';
import { ComunicacionInternaService } from '../../servicios/comunicacion-interna.service';
import { FinanzasRegistrosService } from '../../servicios/finanzas-servicios/finanzas-registros.service';
import { FinanzasCategoriasService } from '../../servicios/finanzas-servicios/finanzas-categorias.service';
import { FinanzasPdfService } from '../../servicios/finanzas-servicios/finanzas-pdf.service';
import { NgxPaginationModule } from 'ngx-pagination';
import { LineasComponent } from '../graficos/lineas/lineas.component';

@Component({
  selector: 'app-registros',
  imports: [
    CurrencyPipe,
    FormsModule,
    NgxPaginationModule,
    NgFor,
    LineasComponent,
  ],
  templateUrl: './registros.component.html',
  styleUrl: './registros.component.css',
})
export class RegistrosComponent {
  constructor(
    private finanzasPdfService: FinanzasPdfService,
    private finanzasCategoriasService: FinanzasCategoriasService,
    private finanzasRegistrosService: FinanzasRegistrosService,
    private comunicacionInternaService: ComunicacionInternaService
  ) {}

  registros: Registro[] = [];
  categorias: Categoria[] = [];

  categoria: string = '';
  tipo: string = '';
  cantidad: number = 0;
  concepto: string = '';

  selectorMeses = false;

  //Lista de meses
  lista_meses = [
    { nombre: 'Todos', valor: 0 },
    { nombre: 'Enero', valor: 1 },
    { nombre: 'Febrero', valor: 2 },
    { nombre: 'Marzo', valor: 3 },
    { nombre: 'Abril', valor: 4 },
    { nombre: 'Mayo', valor: 5 },
    { nombre: 'Junio', valor: 6 },
    { nombre: 'Julio', valor: 7 },
    { nombre: 'Agosto', valor: 8 },
    { nombre: 'Septiembre', valor: 9 },
    { nombre: 'Octubre', valor: 10 },
    { nombre: 'Noviembre', valor: 11 },
    { nombre: 'Diciembre', valor: 12 },
  ];

  anios: AnioRegistro[] = [];
  meses: MesRegistro[] = [];

  mesSeleccionado: number = 0;
  anioSeleccionado: number = 0;

  registroId: number = 0;

  //Pagina de la paginacion
  pagina: number = 1;

  //Tamaño de la paginacion
  selectedPageSize: number = 5;

  ngOnInit() {
    this.getRegistrosUser();
    this.getCategorias();
    this.getAniosRegistros();
    this.getMesesRegistros();
    this.habilitarDropdownMeses();
  }

  // Funcion que comprueba si el dropdown de años está en "Todos", si es así deshabilita el dropdown de meses.
  // Esto hace que solo se puedan buscar registros de meses en base al año y no registros de meses sin importar el año.
  habilitarDropdownMeses() {
    if (this.anioSeleccionado == 0) {
      this.selectorMeses = true;
    } else {
      this.selectorMeses = false;
    }
  }

  //Establece la pagina de la paginacion en 1
  paginacion() {
    this.pagina = 1;
  }

  botonEditar(registroId: number) {
    this.registroId = registroId;
    this.finanzasRegistrosService.getRegistro(this.registroId).subscribe((data) => {
      this.categoria = data.categoria;
      this.concepto = data.concepto;
      this.cantidad = data.cantidad;
      this.tipo = data.tipo;
    });
  }

  actualizarRegistro() {
    this.finanzasRegistrosService.updateRegistro(this.registroId, this.categoria, this.cantidad, this.concepto, this.tipo).subscribe(()=>{
      // Si el año seleccionado es mayor que 0 se obtienen los registros filtrados por año y mes, si no, se obtiene sin ningun filtrado
      // esto previene que al actualizar un registro cuando el filtro está seleccionado no se muestren los resultados sin filtrar, si no que se carguen de nuevo los filtrados
      if (this.anioSeleccionado != 0) {
        this.finanzasRegistrosService
          .filtrarRegistros(this.anioSeleccionado, this.mesSeleccionado)
          .subscribe((data) => {
            this.registros = data.registros;
          });
      }else{
        this.getRegistrosUser();
      }
      Swal.fire({
        position: 'top',
        icon: 'success',
        title: 'Actualizado correctamente',
        showConfirmButton: false,
        timer: 1500,
        toast: true,
      });
      this.comunicacionInternaService.setRefreshData();
    });
  }

  filtrarRegistros(tipo: 'anio' | 'mes') {
    if (tipo === 'anio') {
      this.habilitarDropdownMeses();
      this.mesSeleccionado = 0; // Reiniciar mes al cambiar el año
      this.getMesesRegistros(); // Actualizar los meses disponibles para el nuevo año
    }
    this.finanzasRegistrosService
      .filtrarRegistros(this.anioSeleccionado, this.mesSeleccionado)
      .subscribe((data) => {
        this.registros = data.registros;
        this.paginacion();
      });
  }

  generarPDF() {
    this.finanzasPdfService.generarPDF(this.registros).subscribe((pdf) => {
      const pdfURL = window.URL.createObjectURL(pdf);
      window.open(pdfURL, '_blank'); // Abre en una nueva pestaña
    });
  }

  // Resetea los filtros a su valor por defecto
  resetFiltros() {
    this.mesSeleccionado = 0; // "Todos" en el mes
    this.anioSeleccionado = 0; // "Todos" en el año
    this.getRegistrosUser(); // Obtener todos los registros
    this.habilitarDropdownMeses();
  }

  getAniosRegistros() {
    this.finanzasRegistrosService.getAniosRegistros().subscribe((data) => {
      this.anios = data.registros;
    });
  }

  getMesesRegistros() {
    this.finanzasRegistrosService
      .getMesesRegistros(this.anioSeleccionado)
      .subscribe((data) => {
        this.meses = data.registros;
      });
  }

  getRegistrosPorAnio() {
    if (this.anioSeleccionado == 0) {
      this.getRegistrosUser();
    }
    this.finanzasRegistrosService
      .getRegistrosPorAnio(this.anioSeleccionado)
      .subscribe({
        next: (data) => {
          this.registros = data.registros;
        },
      });
  }

  getRegistrosPorMes() {
    if (this.mesSeleccionado == 0) {
      this.getRegistrosUser();
    }
    this.finanzasRegistrosService
      .getRegistrosPorMes(this.mesSeleccionado)
      .subscribe({
        next: (data) => {
          this.registros = data.registros;
        },
      });
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
    this.finanzasRegistrosService.deleteRegistro(id).subscribe(() => {

      // Si el año seleccionado es mayor que 0 se obtienen los registros filtrados por año y mes, si no, se obtiene sin ningun filtrado
      // esto previene que al eliminar un registro cuando el filtro está seleccionado no se muestren los resultados sin filtrar, si no que se carguen de nuevo los filtrados
      if (this.anioSeleccionado != 0) {
        this.finanzasRegistrosService
          .filtrarRegistros(this.anioSeleccionado, this.mesSeleccionado)
          .subscribe((data) => {
            this.registros = data.registros;
          });
      }else{
        this.getRegistrosUser();
      }
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
        },
      });
  }
}
