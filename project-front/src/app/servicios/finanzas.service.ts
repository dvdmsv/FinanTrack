import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { RegistroPorCategoriaResponse, RegistroUserResponse, SaldoResponse } from '../interfaces/responses';

@Injectable({
  providedIn: 'root'
})
export class FinanzasService {

  constructor(private http: HttpClient) { }
  
  private API_URL = 'http://127.0.0.1:5000';

  getSaldo() {
    return this.http.get<SaldoResponse>(this.API_URL + "/getSaldo");
  }

  getRegistrosPorCategoria() {
    return this.http.get<RegistroPorCategoriaResponse>(this.API_URL + "/getRegistrosPorCategoria");
  }

  getRegistrosUser() {
    return this.http.get<RegistroUserResponse>(this.API_URL + "/getRegistrosUser");
  }
}
