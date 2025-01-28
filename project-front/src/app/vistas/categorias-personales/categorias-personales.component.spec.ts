import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CategoriasPersonalesComponent } from './categorias-personales.component';

describe('CategoriasPersonalesComponent', () => {
  let component: CategoriasPersonalesComponent;
  let fixture: ComponentFixture<CategoriasPersonalesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CategoriasPersonalesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CategoriasPersonalesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
