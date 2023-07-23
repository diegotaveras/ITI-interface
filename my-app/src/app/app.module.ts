import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { InputComponentComponent } from './input-component/input-component.component';
import { PolicyCreatorComponent } from './policy-creator/policy-creator.component';
import { RuleCreatorComponent } from './rule-creator/rule-creator.component';

@NgModule({
  declarations: [
    AppComponent,
    InputComponentComponent,
    PolicyCreatorComponent,
    RuleCreatorComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
