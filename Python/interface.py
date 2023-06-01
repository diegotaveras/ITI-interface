
from __future__ import print_function, unicode_literals
import xml.etree.ElementTree as ET
from PyInquirer import prompt,Separator, Token, style_from_dict

import argparse
from pyfiglet import Figlet

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
        rule = prompt(askRules, style=style)
        
        rule.update({'id': ruleNum})
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
        objectList = prompt(askObjects, style=style)
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
    return prompt(askDescription, style=style)

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
        dictionary = prompt(askDictionary, style=style)
            
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

def RenderTitleText():
    f = Figlet(font='slant')
    print(f.renderText('Policy Creator'))
    
def getArgs():
    parser = argparse.ArgumentParser(description='Create your own policy.xml file.')
    parser.add_argument('--dev', action='store_true',
                        help='enables developer mode')
    return parser.parse_args()


def DevMode():
    policyRuleSet = ET.Element("PolicyRuleSet")
    policyRuleSet.set("dtdVersion","0.1")

    standards = askStandards()      #get Standards to follow 

    rules = askRules()          #get Rules for policy
    for i in range(len(rules)):
        policyRule = ET.SubElement(policyRuleSet, "PolicyRule")
        policyRule.set("name", str(rules[i]['id']))
        policyRule.set("quantifier", str(rules[i]["quantifier"]))
        policyRule.set("evaluate", str(rules[i]["function"]))

        description = ET.SubElement(policyRule, "Description")
        description.text = rules[i]["description"]

        policyRuleSet.append(policyRule)
        print(policyRuleSet.attrib)


    objectLists = askObjects()
    for i in range(len(objectLists)):
        objectList = ET.SubElement(policyRuleSet, "ObjectList")
        objectList.set("name", str(objectLists[i]['name']))
        objectList.set("imported", str(objectLists[i]["imported"]))
        objectList.set("compute", str(objectLists[i]["compute"]))
    

        print(policyRuleSet.attrib)
    
    
    dictionaries = []
    wantDictionary = askIf("dictionary")        #ask if want to add dictionaries
    if wantDictionary["addCustom"]:             
        dictionaries = askDictionary()
        for i in range(len(dictionaries)):
            dictionary = ET.SubElement(policyRuleSet, "Dictionary")
            dictionary.set("name", str(dictionaries[i]['name']))
            dictionary.set("imported", str(dictionaries[i]["imported"]))
            dictionary.set("compute", str(dictionaries[i]["compute"]))


    wantDescription = askIf("description")   #ask if want to add a description
    if (wantDescription['addCustom']):
        description = ET.SubElement(policyRuleSet, "Description")
        description.text = askDescription()['description']




    tree = ET.ElementTree(policyRuleSet)
    # ET.SubElement(policyRuleSet,)
    

    with open("output.xml", 'wb') as file: 
        ET.indent(tree) 
        tree.write(file,xml_declaration=True,encoding='utf-8')

def main():
    RenderTitleText()
    args = getArgs()
    if args.dev:
        DevMode()
        return
    

    

if __name__ == "__main__":
    main()















