import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { RegistroPorCategoriaResponse, SaldoResponse } from '../../interfaces/responses';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class FinanzasSaldoService {

  constructor(private http: HttpClient) { }

  private API_URL = environment.API_URL_DOCKER;
  private SALDO = environment.SALDO;

  getSaldo() {
    return this.http.get<SaldoResponse>(this.API_URL + this.SALDO + "/getSaldo");
  }

  setSaldo(saldo: number) {
    return this.http.post(this.API_URL + this.SALDO + "/setSaldo", {saldo});
  }
}
