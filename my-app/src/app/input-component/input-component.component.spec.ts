import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InputComponentComponent } from './input-component.component';

describe('InputComponentComponent', () => {
  let component: InputComponentComponent;
  let fixture: ComponentFixture<InputComponentComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [InputComponentComponent]
    });
    fixture = TestBed.createComponent(InputComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
