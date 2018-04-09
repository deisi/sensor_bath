#!/usr/bin/env python
"""Script to send sensordata via mqtt."""

import Adafruit_DHT
import paho.mqtt.publish as publish
from time import sleep
from ds18b20 import Ds18b20
import yaml

# Configurations
PIN = 25
SENSOR = 11
BROKER = 'deisi.deiseroth.de'
PORT = 8883
TLS = {'ca_certs': '/etc/ssl/certs/ca-certificates.crt'}
ds18b20 = Ds18b20()
debug = 1

with open('/home/pi/bin/secret.yaml') as secret:
    AUTH = yaml.load(secret)

def read_data():
    hum, temp = Adafruit_DHT.read_retry(SENSOR, PIN)
    temp = round(ds18b20.get_temp()[0], 1)
    return hum, temp

def send_data():
    global HUM_LAST
    global TEMP_LAST
    global LAST_SEND

    hum, temp = read_data()
    if debug:
        print('Read Hum: {} Temp: {}'.format(hum, temp))
    if (hum - HUM_LAST)**2 < 3**2 and LAST_SEND['hum']/INTERVAL <= 1:
        LAST_SEND['hum'] += 1
        hum = None

    if (temp - TEMP_LAST)**2 < 0.3**2 and LAST_SEND['temp']/INTERVAL <= 1:
        LAST_SEND['temp'] += 1
        temp = None

    if hum:
        if debug:
            print('Sending Hum')
        HUM_LAST = hum
        LAST_SEND['hum'] = 0
        publish.single(
            'bad/humidity',
            str(hum),
            hostname=BROKER,
            port=PORT,
            auth=AUTH,
            tls=TLS
        )
    if temp:
        if debug:
            print('Sending Temp')
        TEMP_LAST = temp
        LAST_SEND['temp'] = 0
        publish.single(
            'bad/temperature_one',
            str(temp),
            hostname=BROKER,
            port=PORT,
            auth=AUTH,
            tls=TLS
        )

# Global Variables
HUM_LAST = 80 #%
TEMP_LAST = 15 # degree
STIME = 10 # seconds
LAST_SEND = {'hum' : 0, 'temp': 0} #Counter
INTERVAL = 90 # Counter

# Event Loop
while True:
    send_data()
    sleep(STIME)
