#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
import time
import datetime
import configparser

# libraries
import sys,os
import http.client
import urllib.request, urllib.parse, urllib.error
import json
from sense_hat import SenseHat

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 30

#SERVER
SERVER = "data.sparkfun.com" 
fields = ["humidity", "pressure", "temp"]

#Read the config from file
#config = SafeConfigParser()
config = configparser.ConfigParser()
config.read('config.ini')
publicKey = config.get('main', 'publicKey')
privateKey =  config.get('main', 'privateKey')

sense = SenseHat()
sense.clear()                
print(('Logging sensor measurements to {0} every {1} seconds.'.format(SERVER, FREQUENCY_SECONDS)))
print( 'Press Ctrl-C to quit.')

while True:
        #Correció manual de la temperatura de la CPU
        #readtemp = sense.get_temperature()
        readtemp = sense.get_temperature_from_pressure() 
        t = os.popen('/opt/vc/bin/vcgencmd measure_temp')
        cputemp = t.read()
        cputemp = cputemp.replace('temp=','')
        cputemp = cputemp.replace('\'C\n','')
        cputemp = float(cputemp)
        temp = readtemp - ((cputemp - readtemp) / 1.5)
        print(("%.1f C (metode 1)" % temp))
        #Una altra de les correccions
        t = sense.get_temperature()
        p = sense.get_temperature_from_pressure()
        h = sense.get_temperature_from_humidity()
        temp = ((t+p+h)/3) - (cputemp/5)
        print(("%.1f C (metode 2)" % temp))
        # Attempt to get sensor reading.
        #temp = sense.get_temperature()
        temp = round(temp, 1)
        humidity = sense.get_humidity()
        humidity = round(humidity, 1)
        pressure = sense.get_pressure()
        pressure = round(pressure, 1)
        
        # 8x8 RGB
        sense.clear()
        info = 'Temperature (C): ' + str(temp) + 'Humidity: ' + str(humidity) + 'Pressure: ' + str(pressure)
        #sense.show_message(info, text_colour=[255, 0, 0])
        
        # Print
        print(("Humidity: ", humidity))
        print(("Pressure: ", pressure, "\n"))
        print(("Temperature (C): ", temp))

        data = {}
        data[fields[0]] = humidity
        data[fields[1]] = pressure
        data[fields[2]] = temp
        params = urllib.parse.urlencode(data)

        headers = {} # start with an empty set
        # These are static, should be there every time:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Connection"] = "close"
        headers['Content-length']=str(len(bytes(params, 'utf-8')))
        #headers["Content-Length"] = len(params) # length of data
        headers["Phant-Private-Key"] = privateKey # private key header

        c = http.client.HTTPConnection(SERVER)
        c.request("POST", "/input/" + publicKey + ".txt", params, headers)
        r = c.getresponse() # Get the server's response and print it
        print((r.status, r.reason))
        #Tanco la connexio a cada volta, no se si es el millor
        c.close()

        # Wait 30 seconds before continuing
        #print 'Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME)
        time.sleep(FREQUENCY_SECONDS)


