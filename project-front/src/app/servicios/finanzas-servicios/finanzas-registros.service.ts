import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { AniosRegistrosResponse, GastosPorMesResponse, GetPresupuestosResponse, MesesRegistrosResponse, Registro, RegistroPorCategoriaResponse, RegistroUserResponse } from '../../interfaces/responses';

@Injectable({
  providedIn: 'root'
})
export class FinanzasRegistrosService {

  constructor(private http: HttpClient) { }
  
  private API_URL = environment.API_URL;
  private REGISTRO = environment.REGISTRO;

  getRegistrosPorCategoria() {
    return this.http.get<RegistroPorCategoriaResponse>(this.API_URL + this.REGISTRO + "/getRegistrosPorCategoria");
  }

  getRegistrosPorCategoria2(anio: number, mes: number) {
    return this.http.get<RegistroPorCategoriaResponse>(`${this.API_URL}${this.REGISTRO}/getRegistrosPorCategoria2/${anio}/${mes}`);
  }

  getRegistrosUser() {
    return this.http.get<RegistroUserResponse>(this.API_URL + this.REGISTRO + "/getRegistrosUser");
  }

  getRegistro(idRegistro: number) {
    return this.http.get<Registro>(`${this.API_URL}${this.REGISTRO}/getRegistro/${idRegistro}`);
  }

  updateRegistro(id: number, categoria: string, cantidad: number, concepto: string, tipo: string) {
    return this.http.post(this.API_URL + this.REGISTRO + "/updateRegistro", { id, categoria, cantidad, concepto, tipo });
  }

  getRegistrosPorMes(mes: number) {
    return this.http.get<RegistroUserResponse>(`${this.API_URL}${this.REGISTRO}/getRegistrosPorMes/${mes}`);
  }

  getRegistrosPorAnio(anio: number) {
    return this.http.get<RegistroUserResponse>(`${this.API_URL}${this.REGISTRO}/getRegistrosPorAnio/${anio}`);
  }

  filtrarRegistros(anio: number, tipo: number, mes: number) {
    return this.http.get<RegistroUserResponse>(`${this.API_URL}${this.REGISTRO}/filtrarRegistros/${anio}/${tipo}/${mes}`);
  }

  generarRegistro(categoria: string, tipo: string, cantidad: number, concepto: string, fecha: string) {
    return this.http.post(this.API_URL + this.REGISTRO + "/generarRegistro", {categoria, tipo, cantidad, concepto, fecha});
  }

  deleteRegistro(id: number) {
    return this.http.delete(`${this.API_URL}${this.REGISTRO}/deleteRegistro/${id}`);
  }

  getAniosRegistros() {
    return this.http.get<AniosRegistrosResponse>(this.API_URL + this.REGISTRO + '/getAniosRegistros');
  }

  getMesesRegistros(anio: number) {
    return this.http.get<MesesRegistrosResponse>(`${this.API_URL}${this.REGISTRO}/getMesesRegistros/${anio}`);
  }

  getGastosPorMes(anio: number) {
    return this.http.post<GastosPorMesResponse>(this.API_URL + this.REGISTRO + '/gastos-por-mes', { anio });
  }
}
