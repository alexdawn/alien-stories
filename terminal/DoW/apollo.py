import sys
import os
import random
import time
import datetime

# commtech system for the fort Destroyer of Worlds

def slow_print(text):
    for char in list(text):
        sys.stdout.write(char)
        sys.stdout.flush()
        if char != ' ':
            time.sleep(0.02)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt():
    sys.stdout.write("\n")
    sys.stdout.write(">")
    sys.stdout.flush()

def print_help():
    clear()
    slow_print(
"""Seegson Corp. - A.P.O.L.L.O. TERMINAL SYSTEM (v2.8.0)

USCMC Fort Nebraska, Ariarcus

WARNING Containment Protocol Activated
WARNING Emergency Power A.P.O.L.L.O. in standby mode 

  help                   Displays this help screen
  status                 Base system status report
  log [5 new messages!]  Print incident report
  elevator               Elevator status and travel times
  clear                  Clear screen
  exit                   Shutdown terminal
""")

def print_elevator():
    slow_print("""Elevator
    
    CAR:                  @GROUND
    POWER:        REACTOR OFFLINE
    CNYN DOOR:             CLOSED
    LOCKING CLAMP:         ACTIVE
    
    A.P.O.L.L.O has clearance to
    remove clamps. Ascent time 4 hours
    """)

def print_log():
    slow_print("""Fort logs

* Containment Protocol Activated - Outbreak on SLVL 03
* Interior door:        LOCKED (Major and above)
* Exterior gate:        LOCKED (All ranks)
* Perimeter defence:    ACTIVE
* CAUTION !!! sentry gun IFF disabled
* CAUTION !!! blast hazard
* CAUTION !!! radiation hazard SLVL 02
* NOTICE anti radiation protocol activate
* CAUTION !!! blast  hazard
* CAUTION !!! biological hazard SLVL 03, 02, 01
* S...
* REBOOT
* Initiate core shutdown
* Reactor status:      OFFLINE
* Power status:      EMERGENCY
* CAUTION !!! EMP hazard
* CAUTION !!! radiation hazard SLVL 02, 01
* CAUTION !!! heat hazard SLVL 02
* ERROR !!! radiation protocol failure
* CAUTION !!! Running on EMERGENCY power, rebooting in safe mode
* REBOOT SAFEMODE
* Safemode activate, prior logs may be missing or corrupted
* CAUTION !!! biological aerosol hazard surface, LVL 01, 02, 03
* WARNING sys scan reports hardware failure
""")

def print_status():
    slow_print("""status:
* APOLLO         STANDBY
* CNYN DOOR       LOCKED
* ELEVATOR       OFFLINE, LOCKED SLVL 03, 02
* GUN BTRY        NO-SIG
* OPS            OFFLINE
* PRMTR DEF      !ACTIVE!
* REACTOR        OFFLINE
* STAGING         NO-SIG
* WAR ROOM        NO-SIG
""")

def print_unknown():
    slow_print("Command not recognised\n")

def readcommand():
    for user_input in sys.stdin:
        if user_input == 'exit\n':
            clear()
            break
        commands = {
            'log\n': print_log,
            'status\n': print_status,
            'elevator\n': print_elevator,
            'help\n': print_help,
            'clear\n': clear
        }
        commands.get(user_input, print_unknown)()
        prompt()

def main():
    print_help()
    prompt()
    readcommand()

if __name__ == '__main__':
    main()
