import { TestBed } from '@angular/core/testing';

import { ComunicacionInternaService } from './comunicacion-interna.service';

describe('ComunicacionInternaService', () => {
  let service: ComunicacionInternaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ComunicacionInternaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
