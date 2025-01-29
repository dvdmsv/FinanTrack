import { Component, OnInit } from '@angular/core';
import { AgChartOptions } from 'ag-charts-community';
import { AgCharts } from "ag-charts-angular";
import { FinanzasService } from '../../../servicios/finanzas.service';
import { RegistroPorCategoria } from '../../../interfaces/responses';
import { ComunicacionInternaService } from '../../../servicios/comunicacion-interna.service';

@Component({
  selector: 'app-donut',
  imports: [AgCharts],
  templateUrl: './donut.component.html',
  styleUrl: './donut.component.css',
})
export class DonutComponent implements OnInit {
  registrosPorCategoria: RegistroPorCategoria[] = [];

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

  constructor(private finanzasService: FinanzasService, private comunicacionInternaService: ComunicacionInternaService) {}

  ngOnInit(): void {
    this.cargarRegistrosPorCategoria();
    this.refrescarValores();
  }

  private cargarRegistrosPorCategoria(): void {
    this.finanzasService.getRegistrosPorCategoria().subscribe({
      next: (data) => {
        this.registrosPorCategoria = data.categorias;

        // Reasignamos el objeto para que Angular detecte el cambio
        this.options = {
          ...this.options,
          data: this.registrosPorCategoria,
        };
      },
      error: (err) => {
        console.error('Error al obtener registros por categoría:', err);
      },
    });
  }

  private refrescarValores() {
    this.comunicacionInternaService.refreshData.subscribe(data => {
      if(data == true){
        this.cargarRegistrosPorCategoria();
      }
    });
  }
}
