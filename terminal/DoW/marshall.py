import sys
import os
import random
import time
import datetime

# commtech system for marshall station Destroyer of Worlds

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

def slow_print_help():
    clear()
    slow_print(
"""Weyland-Yutani - Sentinel Civil Security System (v5.6.1)

UA Marshal Station, District East, Ariarcus

  help\tDisplays this help screen
  cam\tJail camera system
  sat\tSpace elevator infrared system
  log\tEmergency service logging system
  comm\tAriarcus Civil Radio (Marshall, Medical, Fire, Rescue)
  rec\tDuty officer records system
  met\tWeather reports
  clear\tClear screen
  exit\tShutdown terminal
""")

def slow_print_jail_cam():
    slow_print("""Feeds:

    Entrance: DEAD
    Bullpen: DEAD
    Interrogation: DEAD
    Holding Area: DEAD
""")

def slow_print_infrared():
    slow_print("""Infrared Satlink
    
    WARNING: Heatsource detected Oil Refinery (North)
        Position: Lat 34.65, Lon -0.03
        Flare Temp: 874\u00b0C
        Ambient Temp: -15\u00b0C
        Date: Today 0442Z
""")

def slow_print_log():
    incident = [
        "Looting", "Armed robbery", "Burglary", "Drunk and disordley", "Bodily harm", "Prank call",
        "Fire", "Sinkhole", "Traffic collision", "Building collapse", "Stranded colonists",
        "Heart attack", "Drug OD", "Missing person"]
    region = [
        "District North", "District East", "District West", "District South", "Wildcatter Park", 
        "Spaceport", "Oblivion Bar"]
    random.seed(10)
    slow_print("Station Call log\n")
    slow_print("\n")
    start_time = datetime.datetime.strptime('10:04:26', "%H:%M:%S")
    log_time = start_time
    for i in range(25):
        log_time -= datetime.timedelta(seconds=random.randrange(60, 60*25))
        slow_print(f"{log_time.strftime('%H%MZ'):>5}\t{random.choice(incident):>20}\t{random.choice(region):>20}\n")
    log_time -= datetime.timedelta(seconds=random.randrange(60, 60*25))
    slow_print(f"{log_time.strftime('%H%MZ'):>5}\t{'Prank call':>20}\t{'District South':>20}\n")
    log_time -= datetime.timedelta(seconds=random.randrange(60, 60*25))
    slow_print(f"{log_time.strftime('%H%MZ'):>5}\t{'Prank call':>20}\t{'Wildcatter Park':>20}\n")
    log_time -= datetime.timedelta(seconds=random.randrange(60, 60*25))
    slow_print(f"{log_time.strftime('%H%MZ'):>5}\t{'Drunk and disordley':>20}\t{'Oblivion Bar':>20}\n")

def slow_print_record():
    slow_print(f"""Station record:

    Cell 01\t\tEmpty
    Cell 02\t\tEmpty
    Cell 03\t\tEmpty
    Cell 04\t\tJohn Doe, M30s, Drunk and Disorderly
    Cell 05\t\tEmpty
    Cell 06\t\tEmpty
    Interrogation\tIvan Stolls, M30s, Sedition

#Last viewed record: Imre Botos

Imre Botos, Male Born {2183-33} [Age 33], native of Ariarcus presumed leader of the Ariarcus Insurgency. Botos a graduate with a BA in Milliary History, was a USCMC Combat Engineer before receiving a honourable discharge three years ago. Last sighting was at Ariarcus Spaceport Arrivals 2180 [3 years ago]. Presumed armed and dangerous. Known associates: Ivan Stolls
""")

def slow_print_met():
    slow_print("""Meteorological Report (1000Z)

Storm front moving in, expect blizzard conditions between 
1200Z and 1400Z hours, storm will ease between 1800Z and 2000Z hours.

Overnight and following day expect overcast and gusty conditions,
temperatures to remain low.
""")

def print_comms():
    slow_print("""Ariarcus Civil Telemetric Radio

[AMF]  [0113] forecast. storm front 70% cert. over and out.
[AMS]  [0349] request SRMF. admissions and deaths. over.
[SRMF] [0352] ack. admitted 3 patients tonight. over
[SRMF] [0732] reporting death of R. Harvey. over.
[AMF]  [0816] signing on. blizzard now 90% cert. update at 1000. over.
[XXX]  [0856] <ERROR UNKNOWN ENCODING>
[AMF]  [1006] blizzard will hit pm. see full forecast on met. over.
[ASP]  [1048] incident. break in at spaceport. marines repairing breach and full sweep of the site. request assistance from CM. over.
[AMS]  [1049] ack. sending over marshalls team. over.
[AMS]  [1055] SRMF respond. you have missed three scheduled reports. over.
""")

def print_secret():
    slow_print("""
Repeating Signal:
    Origin: District North
    Signal:
d0 9e d0 b6 d0 b8 d0 b4
d0 b0 d0 bd d0 b8 d0 b5 
20 d0 b4 d0 be d1 81 d1 
82 d0 b0 d0 b2 d0 ba d0 
b8 20 d0 bf d0 be d1 81 
d1 8b d0 bb d0 ba d0 b8 
Decryption...
Decryption...
Decryption...
Decryption...
Decryption success, UPP code...
    'Ожидание доставки посылки'
Translation...
    'AWAITING PACKAGE DELIVERY'
""")

def print_unknown():
    slow_print("Command not recognised\n")

def readcommand():
    for user_input in sys.stdin:
        if user_input == 'exit\n':
            clear()
            break
        commands = {
            'cam\n': slow_print_jail_cam,
            'sat\n': slow_print_infrared,
            'log\n': slow_print_log,
            'rec\n': slow_print_record,
            'comm\n': print_comms,
            'met\n': slow_print_met,
            'help\n': slow_print_help,
            'decrypt\n': print_secret,
            'clear\n': clear
        }
        commands.get(user_input, print_unknown)()
        prompt()

def main():
    slow_print_help()
    prompt()
    readcommand()

if __name__ == '__main__':
    main()
