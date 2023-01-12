#!/usr/bin/python3
###########################
# Berromator Technologies #
#    Michael Bellander    #
#    michael@berro.se     #
###########################

import os
import requests
import re
import sys
import mysql.connector
from time import sleep
from collections import Counter
import pathlib
import datetime
import csv
import pandas as ps
import argparse
from pyberro import *

key = 'key.txt'
googlemaps = "https://maps.googleapis.com/maps/api/distancematrix/xml?origins="
program_home = '/home/apex/apex-cli/'
protected_home = '/home/apex/protected/'
tempoutput = 'tempoutput.txt'
mysqlconf = 'mysql.cnf'
milrapport = 'milrapport.csv'
mydb = mysql.connector.connect(option_files=protected_home + mysqlconf)

with open(protected_home + key) as f:
    KEY = f.readline()
    f.close

def m_collect_and_indatabase():
    os.system('clear')
    mycursor = mydb.cursor()
    datum = input(hue1 + "Date: ")
    start = input(hue2 + "Start: ")
    stopp = input(hue3 + "Stop: ")
    spec = input(hue4 + "T & R? (Yes / No) ")
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

    print (hue5 + 'Status: ' + Ny_Status)
    print (hue6 + 'Datum: ' + datum + '\n' + hue7 + 'Startadress: ' + start + '\n' + hue8 + 'Stoppadress: ' + stopp + '\n' + hue9 + 'T&R: ' + spec +  '\n' + hue10 + 'Km: ' + Ny_Distans + res)

    file = pathlib.Path(program_home + tempoutput)
    if file.exists ():
        f=open(tempoutput)
        lines=f.readlines()
        f.close
    else:
        print('\n File "' + program_home + tempoutput + '" Doesent exist. Run Collect first')
        return

    ychoice = ['yes', 'Yes', 'YES', 'Y', 'y', 'ja', 'Ja', 'JA', 'J', 'j']
    Continue = input(hue11 + 'Import into the database? (y / n) ')
    if Continue in ychoice:

        if spec in ychoice:
            print (hue12 + 'T&R so we took x2 on km: ' + Ny_Distans + ' when we added it to the database')
            sql = "INSERT INTO milrapport (datum, startadress, stoppadress, t_o_r, km) VALUES (%s, %s, %s, %s, %s * 2)"
        else:
            sql = "INSERT INTO milrapport (datum, startadress, stoppadress, t_o_r, km) VALUES (%s, %s, %s, %s, %s)"

    val = (datum, start, stopp, spec, Ny_Distans)
    mycursor.execute(sql, val)
    mydb.commit()
    sql = "SELECT * FROM apex.milrapport ORDER BY id DESC LIMIT 1"
    mycursor.execute(sql)
    result = mycursor.fetchone()
    print(hue13 + 'Date:', str(result[1]), ' Start:', str(result[2]), ' Stop:', str(result[3]), ' T&R:', str(result[4]), ' Km:', str(result[5]), ' Id:', str(result[6]))
    print (res)
    
    input(hue14 + '\nPush enter to retun to menu' + res)

def m_show_total():
    os.system('clear')
    mycursor = mydb.cursor()
    kmsql = "SELECT SUM(COALESCE(`km`, 0.0)) AS KM FROM milrapport"
    mycursor.execute(kmsql)
    km = mycursor.fetchone()
    print(pinkp2 + 'Total: ' + pinkp2, float(km[0]), pinkp2 + 'Km')

    milsql = "SELECT SUM(COALESCE(`km`, 0.0) /10) AS MIL FROM milrapport"
    mycursor.execute(milsql)
    mil = mycursor.fetchone()
    print(pinkp3 + 'Total: ' + pinkp3, float(mil[0]), pinkp3 + 'Mil')

    seksql = "SELECT SUM(COALESCE(`km`, 0.0) /10 * 9.5) AS SEK FROM milrapport"
    mycursor.execute(seksql)
    sek = mycursor.fetchone()
    print(pinkp4 + 'Total: ' + pinkp4, float(sek[0]), pinkp4 + 'Sek')

    input(pinkp5 + '\nPush enter to retun to menu' + res)

def m_show_all_rows():
    os.system('clear')
    mycursor = mydb.cursor()
    allrowssql = "SELECT * FROM apex.milrapport ORDER BY datum ASC"
    mycursor.execute(allrowssql)
    result = mycursor.fetchall()
    for b in result:
        print(hue1 + 'Date:' + hue2, str(b[1]), ' Start:' + hue3, str(b[2]), ' Stop:' + hue4, str(b[3]), ' T&R:' + hue5, str(b[4]), ' Km:' + hue6, str(b[5]), ' Id:' + hue7, str(b[6]))
    print ('')  

    input(hue1 + '\nPush enter to retun to menu' + res)

def m_show_specific_date():
    os.system('clear')
    date1 = input("From (Ex 2022-12-01): ")
    date2 = input("To   (Ex 2022-12-01): ")
    mycursor = mydb.cursor()
    allrowssql = "SELECT * FROM apex.milrapport WHERE DATE(datum) BETWEEN '"+date1+"' AND '"+date2+"' ORDER BY datum ASC"
    mycursor.execute(allrowssql)
    result = mycursor.fetchall()
    for b in result:
        print('Date: ', str(b[1]), ' Start: ', str(b[2]), ' Stop: ', str(b[3]), ' T&R:', str(b[4]), ' Km:', str(b[5]), ' Id:', str(b[6]))

    mycursor = mydb.cursor()
    kmsql = "SELECT SUM(COALESCE(`km`, 0.0)) AS KM FROM milrapport WHERE DATE(datum) BETWEEN '"+date1+"' AND '"+date2+"'"
    mycursor.execute(kmsql)
    km = mycursor.fetchone()
    print('Total km: ', float(km[0]), 'Km')
    print('')

    milsql = "SELECT SUM(COALESCE(`km`, 0.0) /10) AS MIL FROM milrapport WHERE DATE(datum) BETWEEN '"+date1+"' AND '"+date2+"'"
    mycursor.execute(milsql)
    mil = mycursor.fetchone()
    print('Total mil: ', float(mil[0]), 'Mil')
    print('')

    seksql = "SELECT SUM(COALESCE(`km`, 0.0) /10 * 9.5) AS SEK FROM milrapport WHERE DATE(datum) BETWEEN '"+date1+"' AND '"+date2+"'"
    mycursor.execute(seksql)
    sek = mycursor.fetchone()
    print('Sum sek: ', float(sek[0]), 'Kr')
    print ('')

    input('\nPush enter to retun to menu')

def m_import_csv():
    os.system('clear')
    mycursor = mydb.cursor()
    #cursor = mydb.cursor()

    with open(protected_home + milrapport) as f:
        reader = csv.reader(f)
        for row in reader:
            mycursor.execute("""INSERT INTO milrapport (datum, startadress, stoppadress, km, t_o_r)
                          VALUES(%s, %s, %s, %s, %s)
                       """, row)

    mydb.commit()
    print ('Done')

    input('\nPush enter to retun to menu')

def show_menu():
    print (bggreenpal2 + '')
    print (' ' + bggreenpal3 + '                                                  ' + bggreenpal2 + ' ')
    print (bggreenpal3 + ' '  + bggreenpal5 + ' 1) Collect and insert to database                ' + res + bggreenpal3 + ' ')
    print (bggreenpal5 + ' ' + bggreenpal7 + ' 2) Show totals                                   ' + bggreenpal5 + ' ')
    print (bggreenpal7 + ' ' + bggreenpal9 + ' 3) Show all rows in database                     ' + bggreenpal7 + ' ')
    print (bggreenpal9 + ' ' + bggreenpal11 + ' 4) Show rows in database between specific dates  ' + bggreenpal9 + ' ')
    print (bggreenpal11 + ' ' + bggreenpal12 + ' 5) Import into database from csv file            ' + bggreenpal11 + ' ')
    print (bggreenpal13 + ' ' + bggreenpal13 + ' Q) Quit                                          ' + bggreenpal12 + ' ')

def menu():
    while True:
        os.system('clear')
        show_menu()
        choice = input(bggreenpal13 + ' ' + res + fggreenpal3 + '  Enter your choice:                              ' + bggreenpal13 + ' \n' + res + fggreenpal3).lower()
        print (res)
        if choice == '1':
            m_collect_and_indatabase()
        elif choice == '2':
            m_show_total()
        elif choice == '3':
            m_show_all_rows()
        elif choice == '4':
            m_show_specific_date()
        elif choice == '5':
            m_import_csv()
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

