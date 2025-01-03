import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../servicios/auth.service';
import { Router, RouterModule } from '@angular/router';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-login',
  imports: [FormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent {
  constructor(private authService: AuthService, private router: Router) {}

  username: string = "";
  password: string = "";
  userVacio = "";
  passwordVacio = "";
  error = false;

  login(){
    if(this.username == ""){
      this.userVacio = "Nombre de usuario requerido"
    }
    if(this.password == ""){
      this.passwordVacio = "Password requerido"
    }
    if(this.username != ""  && this.password != ""){
      this.authService.login(this.username, this.password).subscribe({
        next: data => {
          this.authService.setToken(data.token);
          this.authService.currentUserLoginOn.next(true);
          this.router.navigateByUrl('dashboard');
          localStorage.setItem('username', this.username);
          Swal.fire({
            position: 'top-end',
            icon: 'success',
            title: 'Logueado correctamente',
            showConfirmButton: false,
            timer: 1500,
            toast: true,
            timerProgressBar: true
          });
        },
        error: error => {
          console.log(error.status)
          if(error.status == 401){
            this.error = true;
          }
        }
      });
    }
  }

}
