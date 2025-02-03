import { TestBed } from '@angular/core/testing';

import { FinanzasSaldoService } from './finanzas-saldo.service';

describe('FinanzasSaldoService', () => {
  let service: FinanzasSaldoService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FinanzasSaldoService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
