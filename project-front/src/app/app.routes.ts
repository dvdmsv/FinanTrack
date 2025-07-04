import { Routes } from '@angular/router';
import { LoginComponent } from './vistas/login/login.component';
import { DashboardComponent } from './vistas/dashboard/dashboard.component';
import { RegistroComponent } from './vistas/registro/registro.component';
import { authGuard } from './guards/auth.guard';
import { isLoggedGuard } from './guards/is-logged.guard';
import { PerfilComponent } from './vistas/perfil/perfil.component';
import { RegistrosComponent } from './vistas/registros/registros.component';
import { PresupuestosComponent } from './vistas/presupuestos/presupuestos.component';
import { SaldoComponent } from './vistas/saldo/saldo.component';
import { TestDashboardComponent } from './vistas/test-dashboard/test-dashboard.component';
import { CategoriasPersonalesComponent } from './vistas/categorias-personales/categorias-personales.component';
import { DonutComponent } from './vistas/graficos/donut/donut.component';
import { GraficosComponent } from './vistas/graficos/graficos.component';
import { PagosRecurrentesComponent } from './vistas/pagos-recurrentes/pagos-recurrentes.component';
import { LineasComponent } from './vistas/graficos/lineas/lineas.component';

export const routes: Routes = [
    { path: '', component:LoginComponent, canActivate: [isLoggedGuard] },
    { path: 'login', component:LoginComponent, canActivate: [isLoggedGuard]},
    { path: 'registro', component:RegistroComponent, canActivate: [isLoggedGuard]},
    { path: 'dashboard', component:DashboardComponent, canActivate: [authGuard] },
    { path: 'perfil', component:PerfilComponent, canActivate: [authGuard] },
    { path: 'registros', component:RegistrosComponent, canActivate: [authGuard] },
    { path: 'presupuestos', component:PresupuestosComponent, canActivate: [authGuard] },
    { path: 'saldo', component:SaldoComponent, canActivate: [authGuard] },
    { path: 'test-dashboard', component:TestDashboardComponent, canActivate: [authGuard] },
    { path: 'categorias-personales', component:CategoriasPersonalesComponent, canActivate: [authGuard] },
    { path: 'graficos', component:GraficosComponent, canActivate: [authGuard] },
    { path: 'donut', component:DonutComponent, canActivate: [authGuard] },
    { path: 'pagos-recurrentes', component:PagosRecurrentesComponent, canActivate: [authGuard] },
    { path: 'lineas', component:LineasComponent, canActivate: [authGuard] },
    { path: '**', component:DashboardComponent, canActivate: [authGuard] }
];
