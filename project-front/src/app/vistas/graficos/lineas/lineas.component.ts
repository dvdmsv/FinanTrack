import { Component, Input, SimpleChanges } from '@angular/core';
import { FinanzasRegistrosService } from '../../../servicios/finanzas-servicios/finanzas-registros.service';
import { AgCharts } from 'ag-charts-angular';
import { AgChartOptions } from 'ag-charts-types';
import { GastoPorMes, GastosPorMesResponse } from '../../../interfaces/responses';
import { ComunicacionInternaService } from '../../../servicios/comunicacion-interna.service';

@Component({
  selector: 'app-lineas',
  standalone: true,
  imports: [AgCharts],
  templateUrl: './lineas.component.html',
  styleUrl: './lineas.component.css'
})
export class LineasComponent {
  constructor(private finanzasRegistrosService: FinanzasRegistrosService, private comunicacionInternaService: ComunicacionInternaService) {}

  gastosPorMes: GastoPorMes[] = [];

  @Input() anio: number = 0;

  public options: AgChartOptions = {
    title: {
      text: 'Gastos Totales por mes' ,
    },
    data: [],
    series: [
      {
        type: 'line',
        xKey: 'mes',
        yKey: 'gasto',
        yName: 'Gasto'
      },
    ],
    axes: [
      {
        type: 'category',
        position: 'bottom',
        title: { text: 'Mes' },
      },
      {
        type: 'number',
        position: 'left',
        title: { text: 'Cantidad' },
      },
    ],
  };

  ngOnInit() {
    this.getGastosPorMes();
    this.refrescarValores();
  }

  // Detecta cambios en anio o mes y actualiza el gráfico automáticamente
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['anio']) {
      this.getGastosPorMes();
    }
  }

  getGastosPorMes() {
    this.finanzasRegistrosService.getGastosPorMes(this.anio).subscribe((data) => {
      this.gastosPorMes = data.gastoPorMes;
      console.log(this.gastosPorMes)
      // Asigna los datos al gráfico
      this.options = { ...this.options, data: this.gastosPorMes };
      
    });
  }

  private refrescarValores() {
    this.comunicacionInternaService.refreshData.subscribe((data) => {
      if (data == true) {
        this.getGastosPorMes();
      }
    });
  }
}
