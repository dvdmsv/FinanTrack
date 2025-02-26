import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ComunicacionInternaService {

  // Evento para refrescar valores de los componentes que se suscriban
  refreshData = new BehaviorSubject<boolean>(false);

  // Estado del modo oscuro
  darkMode = new BehaviorSubject<boolean>(this.checkDarkMode());

  constructor() { }

  /** Método para activar la actualización de datos */
  setRefreshData() {
    this.refreshData.next(true);
  }
  
  /** Método para cambiar el estado del Dark Mode */
  setDarkMode(isDark: boolean) {
    localStorage.setItem('darkMode', JSON.stringify(isDark));
    this.darkMode.next(isDark);
  }

  /** Método para comprobar el estado del Dark Mode en localStorage */
  private checkDarkMode(): boolean {
    return JSON.parse(localStorage.getItem('darkMode') || 'false');
  }

  /** Método para obtener el valor actual de Dark Mode */
  getDarkMode() {
    return this.darkMode.asObservable();
  }
}
