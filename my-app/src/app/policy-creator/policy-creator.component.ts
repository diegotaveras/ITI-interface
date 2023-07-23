import { Component } from '@angular/core';

class Description {
  description: string;

  constructor(desc: string) {
      this.description = desc;
  }

  UpdateDescription(desc: string) {
      this.description = desc;
  }
}

export class Rule {
  id: number;
  quantifier: string;
  evaluate: string;
  description: Description;

  constructor(id: number) {
      this.id = id;
      this.quantifier = "for_all";
      this.evaluate = "";
      this.description = new Description("");
  }

  setFields(quant: string, evaluate: string, desc: Description) {
      this.quantifier = quant;
      this.evaluate = evaluate;
      this.description = desc;
  }
}

export class ObjectList {
  name: string;
  imported: boolean;
  compute: string;

  constructor(name: string) {
      this.name = name;
      this.imported = true;
      this.compute = "";
  }
  setFields(name:string, imported:boolean, compute:string) {
    this.name = name;
    this.imported = imported;
    this.compute = compute;
  }
}

export class Dictionary {
  name: string;
  imported: boolean;
  compute: string;

  constructor(name: string) {
      this.name = name;
      this.imported = true;
      this.compute = "";
  }

  setFields(name:string, imported:boolean, compute:string) {
    this.name = name;
    this.imported = imported;
    this.compute = compute;
  }
}



@Component({
  selector: 'app-policy-creator',
  templateUrl: './policy-creator.component.html',
  styleUrls: ['./policy-creator.component.css']
})
export class PolicyCreatorComponent {
  rules: Rule[] = [];
  dictionaries: Dictionary[] = [];
  objectLists: ObjectList[] = [];
  description: Description = new Description("");

  
 

}


