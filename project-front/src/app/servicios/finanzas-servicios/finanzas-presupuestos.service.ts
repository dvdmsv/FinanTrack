import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { GetPresupuestosResponse } from '../../interfaces/responses';

@Injectable({
  providedIn: 'root'
})
export class FinanzasPresupuestosService {

  constructor(private http: HttpClient) { }
  
  private API_URL = environment.API_URL_DOCKER;
  private PESUPUESTO = environment.PRESUPUESTO;

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
