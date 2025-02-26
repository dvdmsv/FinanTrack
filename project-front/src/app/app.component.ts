import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { LoginComponent } from "./vistas/login/login.component";
import { NavbarComponent } from "./vistas/navbar/navbar.component";
import { ModoOscuroComponent } from "./vistas/modo-oscuro/modo-oscuro.component";

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, NavbarComponent, ModoOscuroComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'project-front';
}
