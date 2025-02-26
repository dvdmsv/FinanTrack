import { Component } from '@angular/core';
import { FinanzasPagosRecurrentesService } from '../../servicios/finanzas-servicios/finanzas-pagos-recurrentes.service';
import { Categoria, Pagos } from '../../interfaces/responses';
import { CurrencyPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FinanzasCategoriasService } from '../../servicios/finanzas-servicios/finanzas-categorias.service';
import Swal from 'sweetalert2';

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
  intervalo: number = 0;
  fecha: string = '';
  estado: boolean = true;
  pagoRecurrenteId: number = 0;


  ngOnInit() {
    this.getPagosRecurrentes();
    this.getCategorias();
  }

  botonEditar(pagoRecurrenteId: number) {
    this.finanzasPagosService.getPagoRecurrente(pagoRecurrenteId).subscribe((data) => {
      this.pagoRecurrenteId = pagoRecurrenteId;
      this.categoria = data.categoria;
      this.tipo = data.tipo;
      this.cantidad = data.cantidad;
      this.concepto = data.concepto;
      this.frecuencia = data.frecuencia;
      this.intervalo = data.intervalo;
      this.fecha = data.siguiente_pago;
      this.estado = data.estado;
    });
  }

  actualizarPagoRecurrente() {
    this.finanzasPagosService.updatePagoRecurrente(this.pagoRecurrenteId, this.categoria, this.tipo, this.cantidad, this.concepto, this.frecuencia, this.intervalo, this.fecha, this.estado).subscribe((data) => {
      Swal.fire({
        position: 'top',
        icon: 'success',
        title: 'Actualizado correctamente',
        showConfirmButton: false,
        timer: 1500,
        toast: true,
      });
      this.getPagosRecurrentes();
    });
  }

  getPagosRecurrentes() {
    this.finanzasPagosService.getPagosRecurrentes().subscribe((data) => {
      this.pagos = data.pagos;
    });
  }

  agregarPagoRecurrente() {
    this.finanzasPagosService.agregarPagoRecurrente(this.categoria, this.tipo, this.cantidad, this.concepto, this.frecuencia, this.fecha, this.estado, this.intervalo).subscribe(() => {
      this.getPagosRecurrentes();
      Swal.fire({
            position: 'top',
            icon: 'success',
            title: 'Creado correctamente',
            showConfirmButton: false,
            timer: 1500,
            toast: true,
            timerProgressBar: true,
          });
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
