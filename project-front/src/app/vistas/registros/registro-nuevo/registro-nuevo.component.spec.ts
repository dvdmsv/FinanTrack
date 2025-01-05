import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegistroNuevoComponent } from './registro-nuevo.component';

describe('RegistroNuevoComponent', () => {
  let component: RegistroNuevoComponent;
  let fixture: ComponentFixture<RegistroNuevoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RegistroNuevoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RegistroNuevoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
