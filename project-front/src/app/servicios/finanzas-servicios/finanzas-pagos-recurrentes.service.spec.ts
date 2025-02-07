import { TestBed } from '@angular/core/testing';

import { FinanzasPagosRecurrentesService } from './finanzas-pagos-recurrentes.service';

describe('FinanzasPagosRecurrentesService', () => {
  let service: FinanzasPagosRecurrentesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FinanzasPagosRecurrentesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
