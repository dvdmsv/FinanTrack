import { TestBed } from '@angular/core/testing';

import { FinanzasRegistrosService } from './finanzas-registros.service';

describe('FinanzasRegistrosService', () => {
  let service: FinanzasRegistrosService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FinanzasRegistrosService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
