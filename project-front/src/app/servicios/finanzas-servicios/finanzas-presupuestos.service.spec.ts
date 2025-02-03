import { TestBed } from '@angular/core/testing';

import { FinanzasPresupuestosService } from './finanzas-presupuestos.service';

describe('FinanzasPresupuestosService', () => {
  let service: FinanzasPresupuestosService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FinanzasPresupuestosService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
