from __future__ import print_function, unicode_literals
import xml.etree.ElementTree as ET
from PyInquirer import prompt,Separator, Token, style_from_dict

from dev_mode_v0 import DevMode
from user_mode import UserMode
import argparse
from pyfiglet import Figlet
from user_mode import FunctionCreator, PolicyCreator



def RenderTitleText():
    f = Figlet(font='slant')
    print(f.renderText('Policy Creator'))
    
def getArgs():
    parser = argparse.ArgumentParser(description='Create your own policy.xml file.')
    parser.add_argument('--dev', action='store_true',
                        help='enables developer mode')
    parser.add_argument('--function', action='store_true',
                        help='opens function creator')
    parser.add_argument('--policy', action='store_true',
                        help='opens policy creator')
    return parser.parse_args()


def main():
    RenderTitleText()
    args = getArgs()
    if args.dev:
        DevMode()
        return
    if args.function:
        FunctionCreator()
        return
    if args.policy:
        PolicyCreator().EditPolicy()
        
        return
    
    UserMode()
    
  
if __name__ == "__main__":
    main()















