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

program_home = '/home/apex/apex-cli/'

collector = 'collector.py'

parsing = 'parsing.py'

system_name = " Apex "

version = "Version 1.0 "

PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'
HEADER = '\033[95m'
OKBLUE = '\033[94m'
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
        print (BOLD + system_name+version)
        print(''), print('')
        sleep(0.1)
        os.system('clear')
        print(''), print('')
        print (WHITE + system_name+version)
        print(''), print('')
        sleep(0.1)
Logo()

exec(open(program_home + collector).read())

exec(open(program_home + parsing).read())


