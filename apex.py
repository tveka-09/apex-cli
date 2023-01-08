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

# MENY
def m_collect_and_indatabase():
    datum = input("Date: ")
    start = input("Start: ")
    stopp = input("Stop: ")
    spec = input("T & R? (Yes / No) ")
    url = ""+googlemaps+""+start+"&destinations="+stopp+"&departure_time=now&key="+KEY+""

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    with open(program_home + tempoutput, 'w') as f:
        f.write('' +datum + '\n' +start + '\n' +stopp + '\n' + (str(response.text)) +spec + '\n')
        f.close

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

    file = pathlib.Path(program_home + tempoutput)
    if file.exists ():
        f=open(tempoutput)
        lines=f.readlines()
        f.close
    else:
        print('\n File "' + program_home + tempoutput + '" Doesent exist. Run Collect first')
        return

    ychoice = ['yes', 'Yes', 'YES', 'Y', 'y', 'ja', 'Ja', 'JA', 'J', 'j']
    Continue = input('Mata in i databasen? (Ja / Nej) ')
    if Continue in ychoice:
      print('')
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
    
      os.remove(program_home + tempoutput)
    else:
      print ('')
      os.remove(program_home + tempoutput)

    input('\nPush enter to retun to menu')

def m_show_total():
    mycursor = mydb.cursor()
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

    input('\nPush enter to retun to menu')

def m_show_all_rows():
    mycursor = mydb.cursor()
    print('')
    allrowssql = "SELECT * FROM apex.milrapport ORDER BY datum ASC"
    mycursor.execute(allrowssql)
    result = mycursor.fetchall()
    for b in result:
        print('Skapad:', str(b[0]), ' Datum:', str(b[1]), ' Start:', str(b[2]), ' Stopp:', str(b[3]), ' T&R:', str(b[4]), ' Km:', str(b[5]), ' Id:', str(b[6]))
    print ('')  

    input('\nPush enter to retun to menu')

def m_show_specific_date():
    print('')
    date1 = input("From (Ex 2022-12-01): ")
    date2 = input("To   (Ex 2022-12-01): ")
    mycursor = mydb.cursor()
    print('')
    allrowssql = "SELECT * FROM apex.milrapport WHERE DATE(datum) BETWEEN '"+date1+"' AND '"+date2+"' ORDER BY datum ASC"
    mycursor.execute(allrowssql)
    result = mycursor.fetchall()
    for b in result:
        print('Skapad:', str(b[0]), ' Datum:', str(b[1]), ' Start:', str(b[2]), ' Stopp:', str(b[3]), ' T&R:', str(b[4]), ' Km:', str(b[5]), ' Id:', str(b[6]))

    input('\nPush enter to retun to menu')

def show_menu():
    print ('\n1) Collect and insert to database')
    print ('2) Show totals')
    print ('3) Show all rows in database')
    print ('4) Show rows in database between specific dates')
    print ('Q) Quit\n')

def menu():
    while True:
        os.system('clear')
        show_menu()
        choice = input('Enter your choice: ').lower()
        print ('')
        if choice == '1':
            m_collect_and_indatabase()
        elif choice == '2':
            m_show_total()
        elif choice == '3':
            m_show_all_rows()
        elif choice == '4':
            m_show_specific_date()
        elif choice == 'q':
            file = pathlib.Path(program_home + tempoutput)
            if file.exists ():
                os.remove(program_home + tempoutput)
                mydb.close()
                return
            mydb.close()
            return
        else:
            print('\nNot a correct choice, please try again')

if __name__ == '__main__':
    menu()

