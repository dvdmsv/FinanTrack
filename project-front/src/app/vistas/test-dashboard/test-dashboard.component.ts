import { Component } from '@angular/core';
import { DashboardComponent } from "../dashboard/dashboard.component";
import { RegistrosComponent } from "../registros/registros.component";
import { PresupuestosComponent } from "../presupuestos/presupuestos.component";

@Component({
  selector: 'app-test-dashboard',
  imports: [DashboardComponent, RegistrosComponent, PresupuestosComponent],
  templateUrl: './test-dashboard.component.html',
  styleUrl: './test-dashboard.component.css'
})
export class TestDashboardComponent {

}
