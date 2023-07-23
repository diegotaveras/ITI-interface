import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RuleCreatorComponent } from './rule-creator.component';

describe('RuleCreatorComponent', () => {
  let component: RuleCreatorComponent;
  let fixture: ComponentFixture<RuleCreatorComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RuleCreatorComponent]
    });
    fixture = TestBed.createComponent(RuleCreatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
