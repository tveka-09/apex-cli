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
import datetime

key = 'key.txt'

googlemaps = "https://maps.googleapis.com/maps/api/distancematrix/xml?origins="

program_home = '/home/apex/apex-cli/'

protected_home = '/home/apex/protected/'

tempoutput = 'tempoutput.txt'

system_name = " Apex "

version = "Version 1.0 "

mysqlconf = 'mysql.cnf'

mydb = mysql.connector.connect(option_files=protected_home + mysqlconf)

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

with open(protected_home + key) as f:
    KEY = f.readline()
    f.close

def Logo():
    num = 4 
    for _ in range(num):
        os.system('clear')
        print ('\n\n' + RED + system_name+version + '\n\n')
        sleep(0.1)
        os.system('clear')
        print ('\n\n' + BOLD + WHITE + system_name+version)
        sleep(0.1)
Logo()

# MENY
def m_collect():
    datum = input("Datum: ")
    start = input("Startadress: ")
    stopp = input("Stoppadress: ")
    spec = input("T & R? (Ja / Nej) ")
    url = ""+googlemaps+""+start+"&destinations="+stopp+"&departure_time=now&key="+KEY+""

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    with open(program_home + tempoutput, 'w') as f:
        f.write('' +datum + '\n' +start + '\n' +stopp + '\n' + (str(response.text)) +spec + '\n')
        f.close
    input('\nPush enter to retun to menu')

def m_parse():
    file = pathlib.Path(program_home + tempoutput)
    if file.exists ():
        f=open(tempoutput)
        lines=f.readlines()
        f.close
    else:
        print('\n File "' + program_home + tempoutput + '" Doesent exist. Run Collect first')
        return

    datum = re.sub(r"[\n\t\s]*", "", (lines[0]))
    start = re.sub(r"[\n\t]*", "", (lines[1]))
    stopp = re.sub(r"[\n\t]*", "", (lines[2]))
    status = re.sub(r"[\n\t\s]*", "", (lines[5]))
    distans = re.sub(r"[\n\t\s]*", "", (lines[17]))
    spec = re.sub(r"[\n\t\s]*", "", (lines[26]))

    Original_Distans = distans
    characters_to_remove = "<text>km</text>"
    Ny_Distans = Original_Distans
    for character in characters_to_remove:
      Ny_Distans = Ny_Distans.replace(character, "")
    Original_Status = status
    characters_to_remove = "<status></status>"
    Ny_Status = Original_Status
    for character in characters_to_remove:
      Ny_Status = Ny_Status.replace(character, "")

    result = (datum, start, stopp, Ny_Distans, spec + '\n')
    time = datetime.datetime.now()
    skapad = time.strftime("%c")

    print ("")
    print (BOLD +WHITE + 'Status: ' +GREEN  +Ny_Status +END)
    print ("")
    print (BOLD +WHITE + 'Skapad: ' +OKCYAN  +skapad +END + '\n' + 'Datum: ' +OKCYAN +datum +END + '\n' +  'Startadress: ' +OKCYAN +start +END + '\n' +  'Stoppadress: ' +OKCYAN +stopp +END + '\n' +  'T&R: ' +OKCYAN +spec +END + '\n' +  'Km: ' +OKCYAN +Ny_Distans +END)
    print ("")

    ychoice = ['yes', 'Yes', 'YES', 'Y', 'y', 'ja', 'Ja', 'JA', 'J', 'j']
    Continue = input('Mata in i databasen? (Ja / Nej) ')
    if Continue in ychoice:
      print('')
    else:
      print ('')
      print ('Ok, quit.')
      print ('')
      print ('Deleting tempoutput.txt')
      os.remove(program_home + tempoutput)
      print ('')
      sys.exit()

    mycursor = mydb.cursor()
    if spec in ychoice:
      print ('')
      print ('T&R so we took x2 on km: ' +Ny_Distans + ' when we added it to the database')
      print ('')
      sql = "INSERT INTO milrapport (skapad, datum, startadress, stoppadress, t_o_r, km) VALUES (%s, %s, %s, %s, %s, %s * 2)"
    else:
      sql = "INSERT INTO milrapport (skapad, datum, startadress, stoppadress, t_o_r, km) VALUES (%s, %s, %s, %s, %s, %s)"

    val = (skapad, datum, start, stopp, spec, Ny_Distans)
    mycursor.execute(sql, val)
    mydb.commit()
    print ('')
    sql = "SELECT * FROM apex.milrapport ORDER BY id DESC LIMIT 1"
    mycursor.execute(sql)
    result = mycursor.fetchone()
    print('Skapad:', str(result[0]), ' Datum:', str(result[1]), ' Start:', str(result[2]), ' Stopp:', str(result[3]), ' T&R:', str(result[4]), ' Km:', str(result[5]), ' Id:', str(result[6]))
    print ('')
    
    allrows = input('Vill du se alla rader i databasen? (Ja / Nej) ')
    if allrows in ychoice:
      print('')
      allrowssql = "SELECT * FROM apex.milrapport ORDER BY id ASC"
      mycursor.execute(allrowssql)
      result = mycursor.fetchall()
      for b in result:
          print('Skapad:', str(b[0]), ' Datum:', str(b[1]), ' Start:', str(b[2]), ' Stopp:', str(b[3]), ' T&R:', str(b[4]), ' Km:', str(b[5]), ' Id:', str(b[6]))

      print ('')  
    else:
      print ('')

    kmsql = "SELECT SUM(COALESCE(`km`, 0.0)) AS KM FROM milrapport"
    mycursor.execute(kmsql)
    km = mycursor.fetchone()
    print('Total km: ', float(km[0]), 'Km')
    print('')

    milsql = "SELECT SUM(COALESCE(`km`, 0.0) /10) AS MIL FROM milrapport"
    mycursor.execute(milsql)
    mil = mycursor.fetchone()
    print('Total mil: ', float(mil[0]), 'Mil')
    print('')

    seksql = "SELECT SUM(COALESCE(`km`, 0.0) /10 * 9.5) AS SEK FROM milrapport"
    mycursor.execute(seksql)
    sek = mycursor.fetchone()
    print('Sum sek: ', float(sek[0]), 'Kr')
    print ('')
    mydb.close()
    os.remove(program_home + tempoutput)

    input('\nPush enter to retun to menu')

def show_menu():
    print ('\n1) Collect')
    print ('2) Parse')
    print ('Q) Exit\n')

def menu():
    while True:
        os.system('clear')
        show_menu()
        choice = input('Enter your choice: ').lower()
        print ('')
        if choice == '1':
            m_collect()
        elif choice == '2':
            m_parse()
        elif choice == 'q':
            file = pathlib.Path(program_home + tempoutput)
            if file.exists ():
                os.remove(program_home + tempoutput)
                return
            return
        else:
            print('\nNot a correct choice, please try again')

if __name__ == '__main__':
    menu()

