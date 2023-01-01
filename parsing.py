#!/usr/bin/python3
# Apex - parser
# Berromator Technologies
# Michael Bellander - michael@berro.se

import os
import requests
import re
import sys
import mysql.connector
import datetime
from collections import Counter

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

tempoutput = '/home/apex/apex-cli/tempoutput.txt'

protected_home = '/home/apex/protected/'

mysqlconf = 'mysql.cnf'

mydb = mysql.connector.connect(option_files=protected_home + mysqlconf)

f=open(tempoutput)
lines=f.readlines()
f.close

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

ychoice = ['yes','Yes', 'YES', 'Y', 'y', 'Ja', 'JA', 'J', 'j']

Continue = input('Vill du mata in datat i databasen? (Ja / Nej) ')
if Continue in ychoice:
  print('')
else:
  print ('')
  print ('Ok, avslutar scriptet.')
  print ('')
  print ('Tar bort tempoutput.txt')
  os.remove(tempoutput)
  print ('')
  sys.exit()

mycursor = mydb.cursor()

if spec == 'Ja' or spec == 'JA' or spec == 'ja' or spec == 'j' or spec == 'J' or spec == 'Yes' or spec == 'yes' or spec == 'YES' or spec == 'y' or spec == 'Y':
  print ('')
  print ('Eftersom det var T&R så tog vi x2 på km: ' +Ny_Distans + ' när vi matade in det i databasen')
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

allrows = input('Vill du se alla rader i databasen? (Ja eller Nej) ')
if allrows == 'yes' or allrows == 'Yes' or allrows == 'YES' or allrows == 'Y' or allrows == 'y' or allrows == 'Ja' or allrows == 'JA' or allrows == 'J' or allrows == 'j':
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
print('Totalt km: ', float(km[0]), 'Km')
print('')

milsql = "SELECT SUM(COALESCE(`km`, 0.0) /10) AS MIL FROM milrapport"
mycursor.execute(milsql)
mil = mycursor.fetchone()
print('Totalt mil: ', float(mil[0]), 'Mil')
print('')

seksql = "SELECT SUM(COALESCE(`km`, 0.0) /10 * 9.5) AS SEK FROM milrapport"
mycursor.execute(seksql)
sek = mycursor.fetchone()
print('Summa sek: ', float(sek[0]), 'Kr')
print ('')

mydb.close()

os.remove(tempoutput)


