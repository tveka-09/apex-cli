#!/usr/bin/python3
# Apex - collector
# Berromator Technologies
# Michael Bellander - michael@berro.se

import os
import requests
import re
import sys
import mysql.connector

key = '/home/apex/protected/key.txt'

tempoutput = '/home/apex/apex-cli/tempoutput.txt'

googlemaps = "https://maps.googleapis.com/maps/api/distancematrix/xml?origins="

with open(key) as f:
    KEY = f.readline()
    f.close

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


