import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { AniosRegistrosResponse, GetPresupuestosResponse, MesesRegistrosResponse, RegistroPorCategoriaResponse, RegistroUserResponse } from '../../interfaces/responses';

@Injectable({
  providedIn: 'root'
})
export class FinanzasRegistrosService {

  constructor(private http: HttpClient) { }
  
  private API_URL = environment.API_URL_DOCKER;
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

  getRegistrosPorMes(mes: number) {
    return this.http.get<RegistroUserResponse>(`${this.API_URL}${this.REGISTRO}/getRegistrosPorMes/${mes}`);
  }

  getRegistrosPorAnio(anio: number) {
    return this.http.get<RegistroUserResponse>(`${this.API_URL}${this.REGISTRO}/getRegistrosPorAnio/${anio}`);
  }

  filtrarRegistros(anio: number, mes: number) {
    return this.http.get<RegistroUserResponse>(`${this.API_URL}${this.REGISTRO}/filtrarRegistros/${anio}/${mes}`);
  }

  generarRegistro(categoria: string, tipo: string, cantidad: number, concepto: string) {
    return this.http.post(this.API_URL + this.REGISTRO + "/generarRegistro", {categoria, tipo, cantidad, concepto});
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
}
