import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../servicios/auth.service';
import { inject } from '@angular/core';

// Guard para proteger las rutas para que no se acceda cuando se está logueado
export const isLoggedGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
    const router = inject(Router);

     // Si el usuario está logueado se le redirige a dashboard, protegiendo las rutas para los usuarios deslogueados
    if(authService.checkLoginStatus()) {
      router.navigateByUrl('/dashboard');
      return false;
    } else {
      return true;
    }
};

