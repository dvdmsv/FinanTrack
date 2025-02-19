import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { Pagos, PagosResponse } from '../../interfaces/responses';

@Injectable({
  providedIn: 'root'
})
export class FinanzasPagosRecurrentesService {

  constructor(private http: HttpClient) { }
  
  private API_URL = environment.API_URL;
  private PAGOS_RECURRENTES = environment.PAGOS_RECURRENTES;

  getPagosRecurrentes() {
    return this.http.get<PagosResponse>(this.API_URL + this.PAGOS_RECURRENTES + '/getPagosRecurrentes');
  }

  getPagoRecurrente(pagoRecurrenteId: number) {
    return this.http.get<Pagos>(`${this.API_URL}${this.PAGOS_RECURRENTES}/getPagoRecurrente/${pagoRecurrenteId}`);
  }

  updatePagoRecurrente(id: number, categoria: string, tipo: string, cantidad: number, concepto: string, frecuencia: string, intervalo: number, siguiente_pago: string, estado: boolean) {
    return this.http.post(this.API_URL + this.PAGOS_RECURRENTES + '/updatePagoRecurrente', { id, categoria, tipo, cantidad, concepto, frecuencia, intervalo, siguiente_pago, estado });
  }

  modificarEstadoPagoRecurrente(pagoRecurrenteId: number, estado: boolean) {
    return this.http.patch(this.API_URL + this.PAGOS_RECURRENTES + '/modificarEstadoPagoRecurrente', { pagoRecurrenteId, estado });
  }

  eliminarPagoRecurrente(pagoRecurrenteId: number) {
    return this.http.delete(`${this.API_URL}${this.PAGOS_RECURRENTES}/eliminarPagoRecurrente/${pagoRecurrenteId}`);
  }

  agregarPagoRecurrente(categoria: string, tipo: string, cantidad: number, concepto: string, frecuencia: string, fecha: string, estado: boolean, intervalo: number) {
    return this.http.post(this.API_URL + this.PAGOS_RECURRENTES + '/agregarPagoRecurrente', { categoria, tipo, cantidad, concepto, frecuencia, fecha, estado, intervalo });
  }
}
