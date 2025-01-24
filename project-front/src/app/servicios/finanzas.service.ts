import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { GetCategoriasResponse, GetPresupuestosResponse, Registro, RegistroPorCategoriaResponse, RegistroUserResponse, SaldoResponse } from '../interfaces/responses';

@Injectable({
  providedIn: 'root'
})
export class FinanzasService {

  constructor(private http: HttpClient) { }
  
  private API_URL = 'http://127.0.0.1:5000';

  getSaldo() {
    return this.http.get<SaldoResponse>(this.API_URL + "/getSaldo");
  }

  setSaldo(saldo: number) {
    return this.http.post(this.API_URL + "/setSaldo", {saldo});
  }

  getRegistrosPorCategoria() {
    return this.http.get<RegistroPorCategoriaResponse>(this.API_URL + "/getRegistrosPorCategoria");
  }

  getRegistrosUser() {
    return this.http.get<RegistroUserResponse>(this.API_URL + "/getRegistrosUser");
  }

  getCategorias() {
    return this.http.get<GetCategoriasResponse>(this.API_URL + "/getCategorias");
  }

  generarRegistro(categoria: string, tipo: string, cantidad: number, concepto: string) {
    return this.http.post(this.API_URL + "/generarRegistro", {categoria, tipo, cantidad, concepto});
  }

  deleteRegistro(id: number) {
    return this.http.delete(`${this.API_URL}/deleteRegistro/${id}`);
  }

  getPresupuestos() {
    return this.http.get<GetPresupuestosResponse>(this.API_URL + '/getPresupuesto');
  }

  setPresupuesto(categoria: string, porcentaje: number) {
    return this.http.post(this.API_URL + '/setPresupuesto',{ categoria, porcentaje });
  }

  deletePresupuesto(id: number) {
    return this.http.delete(`${this.API_URL}/deletePresupuesto/${id}`);
  }
}
