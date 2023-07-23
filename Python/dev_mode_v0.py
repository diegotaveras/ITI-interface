from __future__ import print_function, unicode_literals
import xml.etree.ElementTree as ET
from PyInquirer import prompt,Separator, Token, style_from_dict
from user_mode import Rule, ObjectList, Dictionary, Description, CreateXMLTree

def askStandards():
    askStandards = [
        {
        'type': 'checkbox',
        'message': 'Select (or do not) the standard(s) to adhere by:',
        'name': 'standards',
        'choices': [
            Separator('Adhere by standard(s)?'),
            {
                'name': 'NIST'
            },
            {
                'name': 'ISO 27001'
            },
            {
                'name': 'SOC2',
            },
            {
                'name': 'NERC-CIP'
            },
            {
                'name': 'HIPAA'
            }, 
            {
                'name': 'GDPR'
            },
            {
                'name': 'FISMA'
            }
            ]
        }

    ]
    standards = prompt(askStandards, style=style)
    return standards

def askRules():
    rules = []
    ruleNum = 1

    askAgain = True
    while (askAgain):
        askRules = [
        {
            'type': 'input',
            'message': 'Give your new rule a name.',
            'name': 'name',
        },
        {
            'type': 'list',
            'name': 'quantifier',
            'message': 'Select the quantifier for satisfying this rule.',
            'choices': ['for_all','not_forall', 'exists', 'not_exists'],
            'filter': lambda val: val.lower()
        },
        {
            'type': 'input',
            'message': 'Give the function to be used.',
            'name': 'function',
        },
        {
            'type': 'input',
            'message': 'Give a description for the policy rule.',
            'name': 'description',
        }
        ]
        continueAsking = [
            
            {
            'type': 'confirm',
            'name': 'addRule',
            'message': 'Want to add another rule?',
            'default': False
            }
        ]
        print("Policy Rule #%s" %ruleNum)
        rule_ans = prompt(askRules, style=style)
        
        rule = Rule(str(ruleNum))
        rule.setFields(rule_ans['quantifier'], rule_ans['function'], Description(rule_ans['description']))
        rules.append(rule)
        continueRules = prompt(continueAsking, style=style)
        askAgain = continueRules['addRule']
        ruleNum = ruleNum + 1
        print(rule)
    return rules

def askObjects():
    objectLists = []
    
    askAgain = True
    while (askAgain):
        askObjects = [
        {
            'type': 'input',
            'message': 'Give your new object list a name',
            'name': 'name',
        },
        {
            'type': 'confirm',
            'name': 'imported',
            'message': 'Will this object list be imported?',
            'default': False
        },
        {
            'type': 'input',
            'message': 'Give the function to be used.',
            'name': 'compute',
        }
        ]
        continueAsking = [
            
            {
            'type': 'confirm',
            'name': 'addList',
            'message': 'Want to add another object list?',
            'default': False
            }
        ]
        objectList_ans = prompt(askObjects, style=style)
        objectList = ObjectList(objectList_ans['name'])
        objectList.setFields(objectList_ans['imported'], objectList_ans['compute'])
        objectLists.append(objectList)
        continueObjects = prompt(continueAsking, style=style)
        askAgain = continueObjects['addList']
        print(objectList)
    return objectLists


def askIf(item):  
    
    addCustom = [
        
        {
        'type': 'confirm',
        'name': 'addCustom',
        'message': 'Want to add a ' + item + ' for this policyRuleSet?',
        'default': False
        }
    ]
        
    return prompt(addCustom, style=style)

def askDescription():
    askDescription = [
        {
            'type': 'input',
            'message': 'Give your description for the PolicyRuleSet',
            'name': 'description',
        }
    ]
    description_ans = prompt(askDescription, style=style)
    description = Description(description_ans['description'])
    return description

def askDictionary():
    dictionaries = []
    askAgain = True
    while askAgain:
        askDictionary = [
            {
                'type': 'input',
                'message': 'Give your dictionary a name',
                'name': 'name',
            },
            {
                'type': 'confirm',
                'name': 'imported',
                'message': 'Will this dictionary be imported?',
                'default': False
            },
            {
                'type': 'input',
                'message': 'Give the function to be used.',
                'name': 'compute',
            }
        ]
        continueAsking = [
            
            {
            'type': 'confirm',
            'name': 'addDictionary',
            'message': 'Want to add another dictionary?',
            'default': False
            }
        ]
        dictionary_ans = prompt(askDictionary, style=style)
        dictionary = Dictionary(dictionary_ans['name'])
        dictionary.setFields(dictionary_ans['imported'], dictionary_ans['compute'])
        dictionaries.append(dictionary)
        continueDictionaries = prompt(continueAsking, style=style)
        askAgain = continueDictionaries['addDictionary']
        print(dictionary)
    
    return dictionaries


  
style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


def DevMode():
    policyRuleSet = ET.Element("PolicyRuleSet")
    policyRuleSet.set("dtdVersion","0.1")

    standards = askStandards()      #get Standards to follow 

    rules = askRules()          #get Rules for policy
    
    objectLists = askObjects()    
    
    dictionaries = []
    wantDictionary = askIf("dictionary")        #ask if want to add dictionaries
    if wantDictionary["addCustom"]:             
        dictionaries = askDictionary()
                    
    description = Description("")       
    wantDescription = askIf("description")  #ask if want to add a description
    if (wantDescription['addCustom']):
        description = askDescription()

    CreateXMLTree(rules, objectLists, dictionaries, description)
