import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ComunicacionInternaService {

  // Evento para refrescar valores de los componentes que se suscriban
  refreshData = new BehaviorSubject<boolean>(false);

  constructor() { }


  setRefreshData() {
    this.refreshData.next(true);
  }
}
