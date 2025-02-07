import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PagosRecurrentesComponent } from './pagos-recurrentes.component';

describe('PagosRecurrentesComponent', () => {
  let component: PagosRecurrentesComponent;
  let fixture: ComponentFixture<PagosRecurrentesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PagosRecurrentesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PagosRecurrentesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
