import { Component } from '@angular/core';
import { AuthService } from '../../servicios/auth.service';
import { Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-registro',
  imports: [FormsModule, RouterModule],
  templateUrl: './registro.component.html',
  styleUrl: './registro.component.css',
})
export class RegistroComponent {
  constructor(private authService: AuthService, private router: Router) {}

  username: string = '';
  password: string = '';
  userVacio = '';
  passwordVacio = '';
  error = false;

  registro() {
    if (this.username == '') {
      this.userVacio = 'Nombre de usuario requerido';
    }
    if (this.password == '') {
      this.passwordVacio = 'Password requerido';
    }
    if (this.username != '' && this.password != '') {
      this.authService.registro(this.username, this.password).subscribe({
        next: (data) => {
          console.log(data.token);
          this.authService.setToken(data.token);
          this.authService.currentUserLoginOn.next(true);
          this.router.navigateByUrl('dashboard');
          localStorage.setItem('username', this.username);
          Swal.fire({
            position: 'top',
            icon: 'success',
            title: 'registrado correctamente',
            showConfirmButton: false,
            timer: 1500,
            toast: true,
            timerProgressBar: true,
          });
        },
        error: (error) => {
          console.log(error.status);
          if (error.status == 409) {
            this.error = true;
          }
        },
      });
    }
  }
}
