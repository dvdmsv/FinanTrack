import { HttpClient } from '@angular/common/http';
import { EmbeddedViewRef, Injectable } from '@angular/core';
import { GetCategoriasResponse, GetPresupuestosResponse, Registro, RegistroPorCategoriaResponse, RegistroUserResponse, SaldoResponse } from '../interfaces/responses';
import { environment } from '../../environments/environment.development';

@Injectable({
  providedIn: 'root'
})
export class FinanzasService {

  constructor(private http: HttpClient) { }
  
  private API_URL = environment.API_URL;
  private CATEGORIA = environment.CATEGORIA;
  private PESUPUESTO = environment.PRESUPUESTO
  private REGISTRO = environment.REGISTRO
  private SALDO = environment.SALDO

  getSaldo() {
    return this.http.get<SaldoResponse>(this.API_URL + this.SALDO + "/getSaldo");
  }

  setSaldo(saldo: number) {
    return this.http.post(this.API_URL + this.SALDO + "/setSaldo", {saldo});
  }

  getRegistrosPorCategoria() {
    return this.http.get<RegistroPorCategoriaResponse>(this.API_URL + this.REGISTRO + "/getRegistrosPorCategoria");
  }

  getRegistrosUser() {
    return this.http.get<RegistroUserResponse>(this.API_URL + this.REGISTRO + "/getRegistrosUser");
  }

  getCategorias() {
    return this.http.get<GetCategoriasResponse>(this.API_URL + this.CATEGORIA + "/getCategorias");
  }

  setCategoria(nombre: string, es_global: boolean) {
    return this.http.post(this.API_URL + this.CATEGORIA + "/setCategoria", {nombre, es_global})
  }

  getCategoriasUnicas() {
    return this.http.get<GetCategoriasResponse>(this.API_URL + this.CATEGORIA + "/getCategoriasUnicas");
  }

  deleteCategoria(id: number) {
    return this.http.delete(`${this.API_URL}${this.CATEGORIA}/deleteCategoria/${id}`);
  }

  generarRegistro(categoria: string, tipo: string, cantidad: number, concepto: string) {
    return this.http.post(this.API_URL + this.REGISTRO + "/generarRegistro", {categoria, tipo, cantidad, concepto});
  }

  deleteRegistro(id: number) {
    return this.http.delete(`${this.API_URL}${this.REGISTRO}/deleteRegistro/${id}`);
  }

  getPresupuestos() {
    return this.http.get<GetPresupuestosResponse>(this.API_URL + this.PESUPUESTO + '/getPresupuesto');
  }

  setPresupuesto(categoria: string, porcentaje: number) {
    return this.http.post(this.API_URL + this.PESUPUESTO + '/setPresupuesto',{ categoria, porcentaje });
  }

  deletePresupuesto(id: number) {
    return this.http.delete(`${this.API_URL}${this.PESUPUESTO}/deletePresupuesto/${id}`);
  }
}
