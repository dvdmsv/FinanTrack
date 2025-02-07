import { Component } from '@angular/core';
import { FinanzasPagosRecurrentesService } from '../../servicios/finanzas-servicios/finanzas-pagos-recurrentes.service';
import { Categoria, Pagos } from '../../interfaces/responses';
import { CurrencyPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FinanzasCategoriasService } from '../../servicios/finanzas-servicios/finanzas-categorias.service';

@Component({
  selector: 'app-pagos-recurrentes',
  imports: [CurrencyPipe, FormsModule],
  templateUrl: './pagos-recurrentes.component.html',
  styleUrl: './pagos-recurrentes.component.css',
})
export class PagosRecurrentesComponent {
  constructor(private finanzasPagosService: FinanzasPagosRecurrentesService, private finanzasCategoriasService: FinanzasCategoriasService) {}

  pagos: Pagos[] = [];
  categorias: Categoria[] = [];
  frecuencias = [
    'Diario',
    'Semanal',
    'Mensual',
    'Anual'
  ]

  categoria: string = "";
  tipo: string = '';
  cantidad: number = 0;
  concepto: string = '';
  frecuencia: string = '';
  fecha: string = '';
  estado: boolean = true;

  ngOnInit() {
    this.getPagosRecurrentes();
    this.getCategorias();
  }

  getPagosRecurrentes() {
    this.finanzasPagosService.getPagosRecurrentes().subscribe((data) => {
      this.pagos = data.pagos;
    });
  }

  agregarPagoRecurrente() {
    this.finanzasPagosService.agregarPagoRecurrente(this.categoria, this.tipo, this.cantidad, this.concepto, this.frecuencia, this.fecha, this.estado).subscribe(() => {
      this.getPagosRecurrentes();
    });
    console.log(`
      Categoría: ${this.categoria}
      Tipo: ${this.tipo}
      Cantidad: ${this.cantidad}
      Concepto: ${this.concepto}
      Frecuencia: ${this.frecuencia}
      Fecha: ${this.fecha}
      Estado: ${this.estado ? 'Activo' : 'Inactivo'}
    `);
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

  modificarEstadoPagoRecurrente(event: Event, pagoRecurrenteId: number) {
    const checkbox = event.target as HTMLInputElement;
    const nuevoEstado = checkbox.checked;

    this.finanzasPagosService.modificarEstadoPagoRecurrente(pagoRecurrenteId, nuevoEstado).subscribe();
  }

  eliminar(pagoRecurrenteId: number) {
    this.finanzasPagosService.eliminarPagoRecurrente(pagoRecurrenteId).subscribe(()=>{
      this.getPagosRecurrentes();
    });
  }
}
