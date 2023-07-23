import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PolicyCreatorComponent } from './policy-creator.component';

describe('PolicyCreatorComponent', () => {
  let component: PolicyCreatorComponent;
  let fixture: ComponentFixture<PolicyCreatorComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PolicyCreatorComponent]
    });
    fixture = TestBed.createComponent(PolicyCreatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
