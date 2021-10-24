import sys
import os
import random
import time
import datetime

from utility import slow_print, print_unknown, prompt, clear

# stop terminal echo
# some sort of ascii graphic
# ANSI control codes for boxes outlines etc...
# autocomplete for commands
# autogen help list

def exit_prog(*args):
    clear()
    sys.exit()

def readcommand():
    for user_input in sys.stdin:
        commands = {
            'clear\n': clear,
            'exit\n': exit_prog
        }
        commands.get(user_input, print_unknown)(*str(user_input).split('\n')[0].split(' '))
        prompt()

def main():
    prompt()
    readcommand()

if __name__ == '__main__':
    main()
