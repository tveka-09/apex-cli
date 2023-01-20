#!/usr/bin/python3
###########################
# Berromator Technologies #
#    Michael Bellander    #
#    michael@berro.se     #
###########################

import os
import requests, json
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
program_home = '/home/apex/apex-cli/'
protected_home = '/home/apex/protected/'
mysqlconf = 'mysql.cnf'
reportfile = 'report.csv'
mydb = mysql.connector.connect(option_files=protected_home + mysqlconf)
url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&"

with open(protected_home + key) as f:
    KEY = f.readline()
    f.close

def m_collect_and_indatabase():
    os.system('clear')
    mycursor = mydb.cursor()
    date = input(hue1 + "\n Date: ")
    start = input(hue2 + " Start: ")
    stop = input(hue3 + " Stop: ")
    t_o_r = input(hue4 + " T & R? (y / n) ")
    r = requests.get(url + "origins=" + start + "&destinations=" + stop + "&key=" + KEY)

    payload={}
    headers = {}

    kilometers = r.json()["rows"][0]["elements"][0]["distance"]["text"]
    status = r.json()["rows"][0]["elements"][0]["status"]

    print (hue5 + ' Status: ' + status)
    print (hue6 + ' Date: ' + date + '\n' + hue7 + ' Start: ' + start + '\n' + hue8 + ' Stop: ' + stop + '\n' + hue9 + ' T&R: ' + t_o_r +  '\n' + hue10 + ' Km: ' + kilometers)

    ychoice = ['yes', 'Yes', 'YES', 'Y', 'y', 'ja', 'Ja', 'JA', 'J', 'j']
    Continue = input(hue11 + ' Import into the database? (y / n) ')
    if Continue in ychoice:

        if t_o_r in ychoice:
            print (hue12 + ' T&R so we took x2 on km: ' + kilometers + ' when we added it to the database')
            sql = "INSERT INTO report (date, startadress, stopadress, t_o_r, km) VALUES (%s, %s, %s, %s, %s * 2)"
        else:
            sql = "INSERT INTO report (date, startadress, stopadress, t_o_r, km) VALUES (%s, %s, %s, %s, %s)"

        val = (date, start, stop, t_o_r, kilometers)
        mycursor.execute(sql, val)
        mydb.commit()
        sql = "SELECT * FROM apex.report ORDER BY id DESC LIMIT 1"
        mycursor.execute(sql)
        result = mycursor.fetchone()
        print ('')
        print(hue13 + ' Date:', str(result[1]), ' Start:', str(result[2]), ' Stop:', str(result[3]), ' T&R:', str(result[4]), ' Km:', str(result[5]), ' Id:', str(result[6]))

    else:
        print (' No database insert')
    
    input(hue14 + '\n Push enter to retun to menu')

def m_show_total():
    os.system('clear')
    mycursor = mydb.cursor()
    kmsql = "SELECT SUM(COALESCE(`km`, 0.0)) AS KM FROM report"
    mycursor.execute(kmsql)
    km = mycursor.fetchone()
    print(hue7 + '\n Total: ', float(km[0]), 'Km')

    milsql = "SELECT SUM(COALESCE(`km`, 0.0) /10) AS MIL FROM report"
    mycursor.execute(milsql)
    mil = mycursor.fetchone()
    print(hue8 + ' Total: ', float(mil[0]), 'Mil')

    seksql = "SELECT SUM(COALESCE(`km`, 0.0) /10 * 9.5) AS SEK FROM report"
    mycursor.execute(seksql)
    sek = mycursor.fetchone()
    print(hue9 + ' Total: ', float(sek[0]), 'Sek')

    input(hue10 + '\n Push enter to retun to menu')

def m_show_all_rows():
    os.system('clear')
    print ('')
    mycursor = mydb.cursor()
    allrowssql = "SELECT * FROM apex.report ORDER BY date ASC"
    mycursor.execute(allrowssql)
    result = mycursor.fetchall()
    for b in result:
        print(hue1 + ' Date:' + hue2, str(b[1]), ' Start:' + hue3, str(b[2]), ' Stop:' + hue4, str(b[3]), ' T&R:' + hue5, str(b[4]), ' Km:' + hue6, str(b[5]), ' Id:' + hue7, str(b[6]))

    input(hue1 + '\n Push enter to retun to menu')

def m_show_specific_date():
    os.system('clear')
    date1 = input(hue1 + "\n From (Ex 2022-12-01): ")
    date2 = input(hue2 + " To   (Ex 2022-12-01): ")
    print ('')
    mycursor = mydb.cursor()
    allrowssql = "SELECT * FROM apex.report WHERE DATE(date) BETWEEN '"+date1+"' AND '"+date2+"' ORDER BY date ASC"
    mycursor.execute(allrowssql)
    result = mycursor.fetchall()
    for b in result:
        print(hue3 + ' Date: ', str(b[1]), ' Start: ', str(b[2]), ' Stop: ', str(b[3]), ' T&R:', str(b[4]), ' Km:', str(b[5]), ' Id:', str(b[6]))

    mycursor = mydb.cursor()
    kmsql = "SELECT SUM(COALESCE(`km`, 0.0)) AS KM FROM report WHERE DATE(date) BETWEEN '"+date1+"' AND '"+date2+"'"
    mycursor.execute(kmsql)
    km = mycursor.fetchone()
    print(hue4 + '\n Total km: ', float(km[0]), 'Km')

    milsql = "SELECT SUM(COALESCE(`km`, 0.0) /10) AS MIL FROM report WHERE DATE(date) BETWEEN '"+date1+"' AND '"+date2+"'"
    mycursor.execute(milsql)
    mil = mycursor.fetchone()
    print(hue5 + ' Total mil: ', float(mil[0]), 'Mil')

    seksql = "SELECT SUM(COALESCE(`km`, 0.0) /10 * 9.5) AS SEK FROM report WHERE DATE(date) BETWEEN '"+date1+"' AND '"+date2+"'"
    mycursor.execute(seksql)
    sek = mycursor.fetchone()
    print(hue6 + ' Sum sek: ', float(sek[0]), 'Kr')

    input(hue7 + '\n Push enter to retun to menu')

def m_import_csv():
    os.system('clear')
    print (hue1 + '\n Below rows read from file: "' + protected_home + reportfile + '" and imported into the database:\n')
    mycursor = mydb.cursor()

    with open(protected_home + reportfile) as f:
        reader = csv.reader(f)
        for row in reader:
            mycursor.execute("""INSERT INTO tempimport (tempdate, tempstart, tempstop, tempkm, temptr)
                          VALUES(%s, %s, %s, %s, %s)
                       """, row), print(hue1 + ' Date:' + hue2, str(row[0]), '\t' +  'Start:' + hue3, str(row[1]), '\t\t' + 'Stop:' + hue4, str(row[2]), '\t' + 'Km:' + hue6, str(row[3]), '\t' + 'T&R:' + hue5, str(row[4]))

    mydb.commit()
    input(hue5 + '\n Push enter to retun to menu')

def m_tempdb_to_realdb():
    os.system('clear')
    print (hue1 + '\n Tempdb -> RealDB\n')
    mycursor = mydb.cursor()
    allrowssql = "SELECT * FROM apex.tempimport ORDER BY tempdate ASC"
    mycursor.execute(allrowssql)
    result = mycursor.fetchall()
    for b in result:
        date = str(b[1])
        start = str(b[2])
        stop = str(b[3])
        tr = str(b[4])
        km = str(b[5])
        id = str(b[6])
        r = requests.get(url + "origins=" + start + "&destinations=" + stop + "&key=" + KEY)
        payload={}
        headers = {}
        kilometers = r.json()["rows"][0]["elements"][0]["distance"]["text"]
        status = r.json()["rows"][0]["elements"][0]["status"]
        #x = r.json()
        #print (x)

        print(hue1 + date + hue2 + '\tStart: ' + start + hue3 + '\tStop: ' + stop + hue4 + '\tToR: ' + tr + hue5 + '\tKm: ' + kilometers + hue6 + '\tStatus: ' + status)

    input(hue5 + '\n Push enter to retun to menu')

def show_menu():
    print (hue1 + '\n 1) Insert by date')
    print (hue2 + ' 2) Show totals')
    print (hue3 + ' 3) Show all rows')
    print (hue4 + ' 4) Show rows between specific dates')
    print (hue5 + ' 5) Bulk import from csv file')
    print (hue6 + ' 6) Tempdb to Realdb')
    print (hue7 + ' Q) Quit')

def menu():
    while True:
        os.system('clear')
        show_menu()
        choice = input(hue6 + ' Enter your choice: ').lower()
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
        elif choice == '6':
            m_tempdb_to_realdb()
        elif choice == 'q':
            mydb.close()
            print ('')
            return
        else:
            print('\nNot a correct choice, please try again')

if __name__ == '__main__':
    menu()

