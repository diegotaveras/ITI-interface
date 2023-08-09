from __future__ import print_function, unicode_literals
import xml.etree.ElementTree as ET
from PyInquirer import prompt,Separator, Token, style_from_dict
import sys
from dev_mode_v0 import DevMode
from user_mode import UserMode
import argparse
from pyfiglet import Figlet
from user_mode import FunctionCreator, PolicyCreator, PolicyPublisher, PolicyEvaluator, RuleGroupCreator, CreatePolicyFile



def RenderTitleText():
    f = Figlet(font='slant')
    print(f.renderText('Policy Creator'))
    
def getArgs():
    parser = argparse.ArgumentParser(description='Create your own policy.xml file.')
    parser.add_argument('--dev', action='store_true',
                        help='enables developer mode')
    parser.add_argument('--create_policy', action='store_true',
                        help='opens policy creator')
    parser.add_argument('--publish_policy', action='store_true',
                        help='opens policy publisher')
    parser.add_argument('--evaluate_policy', action='store_true',
                        help='opens policy evaluator')
    parser.add_argument('--create_function', action='store_true',
                        help='opens function creator')
    parser.add_argument('--create_rulegroup', action='store_true',
                        help='opens rule group creator')
    
    return parser.parse_args()


def main():
    RenderTitleText()
    args = getArgs()
    if not len(sys.argv) > 1:
        UserMode()
        
    if args.create_policy:
        creator = PolicyCreator()
        creator.EditPolicy()
        CreatePolicyFile([creator.policy])
    if args.publish_policy:
        PolicyPublisher()
    if args.evaluate_policy:
        PolicyEvaluator()
    if args.create_function:
        FunctionCreator()
    if args.create_rulegroup:
        RuleGroupCreator()

           
  
if __name__ == "__main__":
    main()















