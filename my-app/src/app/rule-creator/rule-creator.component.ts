import { Component, HostListener} from '@angular/core';
import { Rule } from 'src/app/policy-creator/policy-creator.component';

@Component({
  selector: 'app-rule-creator',
  templateUrl: './rule-creator.component.html',
  styleUrls: ['./rule-creator.component.css']
})
export class RuleCreatorComponent {
  rules:Rule[] = []
  ruleNum = 1
  rightClickMenuPositionX = 0;
  rightClickMenuPositionY = 0;
  showDeleteOption: boolean = false;
  selectedRuleId: number = NaN;

  AddRule() {
    this.rules.push(new Rule(this.ruleNum))
    console.log(this.rules)
    this.ruleNum += 1
  }

  getRightClickMenuStyle() {
    return {
      position: 'fixed',
      left: `${this.rightClickMenuPositionX}px`,
      top: `${this.rightClickMenuPositionY}px`
    }
  }

  DeleteOption(e:any, id: number) {
    this.showDeleteOption = true;
    this.selectedRuleId = id;
    for (let i = 0; i < this.rules.length; i++) {
      if (this.rules[i].id  == id) {
        this.rules.splice(i, 1);

      }
      if (this.rules[i].id > id) {
        this.rules[i].id = i + 1;
      }
    }
    
    this.ruleNum = this.rules.length + 1
    this.rightClickMenuPositionX = e.clientX;
    this.rightClickMenuPositionY = e.clientY;
    return true

  }
  
}
