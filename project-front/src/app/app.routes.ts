import { Routes } from '@angular/router';
import { LoginComponent } from './vistas/login/login.component';
import { DashboardComponent } from './vistas/dashboard/dashboard.component';
import { RegistroComponent } from './vistas/registro/registro.component';
import { authGuard } from './guards/auth.guard';
import { isLoggedGuard } from './guards/is-logged.guard';
import { PerfilComponent } from './vistas/perfil/perfil.component';
import { RegistrosComponent } from './vistas/registros/registros.component';
import { RegistroNuevoComponent } from './vistas/registros/registro-nuevo/registro-nuevo.component';

export const routes: Routes = [
    { path: '', component:LoginComponent, canActivate: [isLoggedGuard] },
    { path: 'login', component:LoginComponent, canActivate: [isLoggedGuard]},
    { path: 'registro', component:RegistroComponent, canActivate: [isLoggedGuard]},
    { path: 'dashboard', component:DashboardComponent, canActivate: [authGuard] },
    { path: 'perfil', component:PerfilComponent, canActivate: [authGuard] },
    { path: 'registros', component:RegistrosComponent, canActivate: [authGuard] },
    { path: 'registroNuevo', component:RegistroNuevoComponent, canActivate: [authGuard] }
];
