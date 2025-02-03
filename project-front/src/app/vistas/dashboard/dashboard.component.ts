import { Component, OnInit } from '@angular/core';
import { AnioRegistro, MesRegistro, RegistroPorCategoria } from '../../interfaces/responses';
import { CurrencyPipe } from '@angular/common';
import { ComunicacionInternaService } from '../../servicios/comunicacion-interna.service';
import { DonutComponent } from '../graficos/donut/donut.component';
import { FinanzasRegistrosService } from '../../servicios/finanzas-servicios/finanzas-registros.service';
import { FormsModule, NgForm } from '@angular/forms';

@Component({
  selector: 'app-dashboard',
  imports: [CurrencyPipe, DonutComponent, FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  // Array de los registros por categoría
  registrosPorCategoria: RegistroPorCategoria[] = [];
  // Gasto total de los registros por categoría
  gastoTotal: number = 0;

    //Lista de meses
  lista_meses = [
    { nombre: "Todos", valor: 0 },
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

  // Años y meses donde hay registros, para luego usarlos como opciones en los dropdown de la plantilla
  anios: AnioRegistro[] = [];
  meses: MesRegistro[] = [];

  // Años y meses seleccionados en los dropdown de la plantilla
  mesSeleccionado: number = 0
  anioSeleccionado: number = 0

  constructor(private finanzasRegistrosService: FinanzasRegistrosService, private comunicacionInternaService: ComunicacionInternaService) {}

  ngOnInit(): void {
    this.cargarRegistrosPorCategoria();
    this.getAniosRegistros();
    this.getMesesRegistros();
    this.refrescarValores();
  }

  // Funcion que filtra los registros por categoría en base al año y al mes seleccionado
  filtrarRegistros(tipo: 'anio' | 'mes') {
    if (tipo === 'anio') {
      this.mesSeleccionado = 0; // Reiniciar mes al cambiar el año
      this.getMesesRegistros(); // Actualizar los meses disponibles para el nuevo año
    }
  
    this.finanzasRegistrosService.getRegistrosPorCategoria2(this.anioSeleccionado, this.mesSeleccionado)
      .subscribe((data) => {
  
        this.registrosPorCategoria = data.categorias;
  
        // Calcular el gasto total de todas las categorías
        this.gastoTotal = this.registrosPorCategoria.reduce((acc, registro) => acc + registro.total_cantidad, 0);
      });
  }
  

  // Resetea los filtros a su valor por defecto
  resetFiltros() {
    this.mesSeleccionado = 0;  // "Todos" en el mes
    this.anioSeleccionado = 0; // "Todos" en el año
    this.cargarRegistrosPorCategoria();   // Obtener todos los registros
  }

  // Obtiene los años donde hay registros disponibles
  getAniosRegistros() {
    this.finanzasRegistrosService.getAniosRegistros().subscribe((data)=>{
      this.anios = data.registros;
    })
  }

  // Obtiene los meses donde hay registros disponibles
  getMesesRegistros() {
    this.finanzasRegistrosService.getMesesRegistros(this.anioSeleccionado).subscribe((data)=>{
      this.meses = data.registros;
    })
  }

  // Obtiene los registros por categoría
  private cargarRegistrosPorCategoria(): void {
    this.finanzasRegistrosService.getRegistrosPorCategoria().subscribe({
      next: (data) => {
        this.registrosPorCategoria = data.categorias;

        // Obtener el gasto total de todas las categorías
        this.gastoTotal = 0;
        this.registrosPorCategoria.forEach(registro => {
          this.gastoTotal += registro.total_cantidad;
        });
        
      },
      error: (err) => {
        console.error('Error al obtener registros por categoría:', err);
      }
    });
  }

  // Función que observa si debe refrescar sus valores
  private refrescarValores() {
    this.comunicacionInternaService.refreshData.subscribe(data => {
      if(data == true){
        this.cargarRegistrosPorCategoria();
      }
    });
  }
}
