import { Component, Input, OnInit, SimpleChanges } from '@angular/core';
import { AgChartOptions } from 'ag-charts-community';
import { AgCharts } from "ag-charts-angular";
import { RegistroPorCategoria } from '../../../interfaces/responses';
import { ComunicacionInternaService } from '../../../servicios/comunicacion-interna.service';
import { FinanzasRegistrosService } from '../../../servicios/finanzas-servicios/finanzas-registros.service';

@Component({
  selector: 'app-donut',
  imports: [AgCharts],
  templateUrl: './donut.component.html',
  styleUrl: './donut.component.css',
})
export class DonutComponent implements OnInit {
  registrosPorCategoria: RegistroPorCategoria[] = [];

  @Input() anio: number = 0;
  @Input() mes: number = 0;

  public options: AgChartOptions = {
    data: [],
    title: {
      text: 'Composición de los gastos',
    },
    series: [
      {
        type: 'donut',
        calloutLabelKey: 'categoria',
        angleKey: 'total_cantidad',
        innerRadiusRatio: 0.5,
      },
    ],
  };

  constructor(private finanzasRegistrosService: FinanzasRegistrosService, private comunicacionInternaService: ComunicacionInternaService) {}

  ngOnInit(): void {
    this.filtrarRegistros();
    this.refrescarValores();
  }

   // Detecta cambios en anio o mes y actualiza el gráfico automáticamente
   ngOnChanges(changes: SimpleChanges): void {
    if (changes['anio'] || changes['mes']) {
      this.filtrarRegistros();
    }
  }

  filtrarRegistros() {
    this.finanzasRegistrosService.getRegistrosPorCategoria2(this.anio, this.mes)
      .subscribe((data) => {
  
        this.registrosPorCategoria = data.categorias;

        // Reasignamos el objeto para que Angular detecte el cambio
        this.options = {
          ...this.options,
          data: this.registrosPorCategoria,
        };
      });
  }

  private refrescarValores() {
    this.comunicacionInternaService.refreshData.subscribe(data => {
      if(data == true){
        this.filtrarRegistros();
      }
    });
  }
}
