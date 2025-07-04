import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestDashboardComponent } from './test-dashboard.component';

describe('TestDashboardComponent', () => {
  let component: TestDashboardComponent;
  let fixture: ComponentFixture<TestDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TestDashboardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TestDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
