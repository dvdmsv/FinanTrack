import { TestBed } from '@angular/core/testing';

import { FinanzasCategoriasService } from './finanzas-categorias.service';

describe('FinanzasCategoriasService', () => {
  let service: FinanzasCategoriasService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FinanzasCategoriasService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
