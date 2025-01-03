import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../servicios/auth.service';
import { inject } from '@angular/core';

// Guard para proteger las rutas si no está logueado
export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if(authService.checkLoginStatus()) {
    return true
  } else {
    router.navigateByUrl('/login');
    return false;
  }
};
