import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../servicios/auth.service';

@Component({
  selector: 'app-perfil',
  imports: [FormsModule],
  templateUrl: './perfil.component.html',
  styleUrl: './perfil.component.css'
})
export class PerfilComponent {
  constructor(private authService: AuthService) {}

  username: string = "";
  password: string = "";
  editar: boolean = false;

  ngOnInit() {
    this.authService.getUserData().subscribe({
      next: (userData) => {
        this.username = userData.user_data.username;
      }
    });
  }

  setEditar() {
    this.editar = !this.editar
  }
}
