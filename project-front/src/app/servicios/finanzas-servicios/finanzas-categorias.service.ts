import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { GetCategoriasResponse } from '../../interfaces/responses';

@Injectable({
  providedIn: 'root'
})
export class FinanzasCategoriasService {

  constructor(private http: HttpClient) { }
  
  private API_URL = environment.API_URL_DOCKER;
  private CATEGORIA = environment.CATEGORIA;

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
}
