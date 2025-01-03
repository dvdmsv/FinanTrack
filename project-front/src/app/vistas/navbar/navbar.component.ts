import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../servicios/auth.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
})
export class NavbarComponent {
  constructor(private authService: AuthService, private router: Router) {}

  isLogged: boolean = false;
  username = localStorage.getItem('username');

  ngOnInit() {
    this.authService.currentUserLoginOn.subscribe({
      next: (userLogin) => {
        this.isLogged = userLogin;
      },
    });
  }

  logout() {
    this.authService.logout();
    Swal.fire({
      position: 'top-end',
      icon: 'info',
      title: 'Cerrando sesión',
      showConfirmButton: false,
      timer: 1500,
      toast: true,
      timerProgressBar: true,
    });
  }
}
