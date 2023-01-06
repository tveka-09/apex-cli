#!/usr/bin/python3
# Apex
# Berromator Technologies
# Michael Bellander - michael@berro.se

import os
import requests
import re
import sys
import mysql.connector
from time import sleep
from collections import Counter
import pathlib

key = '/home/apex/protected/key.txt'

tempoutput = '/home/apex/apex-cli/tempoutput.txt'

googlemaps = "https://maps.googleapis.com/maps/api/distancematrix/xml?origins="

program_home = '/home/apex/apex-cli/'

collector = 'collector.py'

parsing = 'parsing.py'

system_name = " Apex "

version = "Version 1.0 "

with open(key) as f:
    KEY = f.readline()
    f.close

PURPLE = '\033[95m'
CYAN = '\033[96m'
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
BOLD = '\033[1m'
END = '\033[0m'
HEADER = '\033[95m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
WHITE =  '\u001b[37m'

def Logo():
    num = 10
    for _ in range(num):
        os.system('clear')
        print(''), print('')
        print (BOLD + WHITE + system_name+version)
        print(''), print('')
        sleep(0.1)
        os.system('clear')
        print(''), print('')
        print (RED + system_name+version)
        print(''), print('')
        sleep(0.1)
Logo()

# MENY
def m_collector():
    print('\nRunning Collector \n')
    datum = input("Datum: ")
    start = input("Startadress: ")
    stopp = input("Stoppadress: ")
    spec = input("T & R? (Ja / Nej) ")
    url = ""+googlemaps+""+start+"&destinations="+stopp+"&departure_time=now&key="+KEY+""

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    with open(tempoutput, 'w') as f:
        f.write('' +datum + '\n' +start + '\n' +stopp + '\n' + (str(response.text)) +spec + '\n')
        f.close
    input('\nPush enter to retun to menu')

def m_parsing():
    print('\nRunning Parsing \n')
    exec(open(program_home + parsing).read())
    input('\nPush enter to retun to menu')

def show_menu():
    print ('\n1) Collector')
    print ('2) Parsing')
    print ('Q) Exit\n')

def menu():
    while True:
        show_menu()
        choice = input('Enter your choice: ').lower()
        if choice == '1':
            m_collector()
        elif choice == '2':
            m_parsing()
        elif choice == 'q':
            file = pathlib.Path(tempoutput)
            if file.exists ():
                os.remove(tempoutput)
                return
            return
        else:
            print(f'Not a correct choice: <{choice}>,try again')

if __name__ == '__main__':
    menu()


