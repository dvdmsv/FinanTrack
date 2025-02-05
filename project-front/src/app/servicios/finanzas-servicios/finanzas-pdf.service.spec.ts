import { TestBed } from '@angular/core/testing';

import { FinanzasPdfService } from './finanzas-pdf.service';

describe('FinanzasPdfService', () => {
  let service: FinanzasPdfService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FinanzasPdfService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
