import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-input-component',
  templateUrl: './input-component.component.html', 
  styleUrls: ['./input-component.component.css']
})
export class InputComponentComponent {
  @Output() filesSelected = new EventEmitter<FileList>();

  handleFileChange(event: Event) {
    const inputElement = event.target as HTMLInputElement;
    if (inputElement.files) {
      this.filesSelected.emit(inputElement.files);
    }
  }
}
