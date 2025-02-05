import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { Registro } from '../../interfaces/responses';

@Injectable({
  providedIn: 'root'
})
export class FinanzasPdfService {

  constructor(private http: HttpClient) { }

  private API_URL = environment.API_URL;
  private PDF = environment.PDF;

  generarPDF(registros: Registro[]) {
    return this.http.post(this.API_URL + this.PDF + '/generarPdf', { registros }, { responseType: 'blob' });
  }
}
