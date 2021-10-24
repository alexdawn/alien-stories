import sys
import os
import time

CHAR_DELAY = 0.02

def slow_print(text):
    for char in list(text):
        sys.stdout.write(char)
        sys.stdout.flush()
        if char != ' ':
            time.sleep(CHAR_DELAY)


def clear(*args):
    os.system('cls' if os.name == 'nt' else 'clear')


def prompt():
    sys.stdout.write("\n")
    sys.stdout.write(">")
    sys.stdout.flush()


def print_unknown(*args):
    slow_print(f"Command '{args[0]}' not recognised\n")
