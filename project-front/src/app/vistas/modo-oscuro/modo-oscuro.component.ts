import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ComunicacionInternaService } from '../../servicios/comunicacion-interna.service';

@Component({
  selector: 'app-modo-oscuro',
  imports: [FormsModule],
  templateUrl: './modo-oscuro.component.html',
  styleUrl: './modo-oscuro.component.css',
})
export class ModoOscuroComponent {
  constructor(private comunicacionInternService: ComunicacionInternaService) {}

  darkMode: boolean = false;

  ngOnInit() {
    this.comunicacionInternService.getDarkMode().subscribe(darkMode => {
      this.darkMode = darkMode;
    });
  }

  setDarkMode() {
    if (this.darkMode) {
      this.comunicacionInternService.setDarkMode(true)
      document.body.classList.add("dark-theme");
    } else {
      this.comunicacionInternService.setDarkMode(false)
      document.body.classList.remove("dark-theme");
    }
  }
}
