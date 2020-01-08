#!/usr/bin/env python
# coding: utf-8

import time
import machine
import usocket
import os
import gc
from json import dumps
from ntptime import settime
from umqtt.simple import MQTTClient
import config
import functions
from pir import PirSensor

class Client:
    
    def __init__(self):
        self.client = MQTTClient(config.MQTT['SENSOR_ID'], config.MQTT['SERVER'], config.MQTT['PORT'], config.MQTT['USER'], config.MQTT['PASSWD'], config.MQTT['KEEPALIVE'])
        self.ps = PirSensor()     
          
    def send2broker(self):
        while True:
            if self.ps.catch_motion():
                structure = {'sensor_id': config.MQTT['SENSOR_ID'], \
                        'timestamp': self.sync_time(), \
                        'value': 1, \
                        'status': 'ok', \
                        'quantity': config.MQTT['QUANTITY'], \
                        'location': config.MQTT['LOCATION'], \
                        'owner': config.MQTT['OWNER']}
                self.mqtt_msg(structure)
                break
            time.sleep_ms(10)

    def sync_time(self):
        GMT = time.mktime(time.localtime()) + 3600
        (year, mon, mday, hour, minute, sec, wd, yd) = time.localtime(GMT)          
        converted_time = (str(year) + '-' + "{:02d}".format(mon) + '-' + "{:02d}".format(mday) + ' ' + "{:02d}".format(hour) + ':' + "{:02d}".format(minute) + ':' + "{:02d}".format(sec))
        return converted_time
    
    def mqtt_msg(self, structure):
        self.client.connect()
        self.client.publish(config.MQTT['MOTION_TOPIC'], dumps(structure))
        self.client.disconnect()
        
    def publish(self):
        while True:
            try:
                if gc.mem_free() < 20000:
                    gc.collect()
                a = usocket.getaddrinfo('www.google.com',80)[0][-1]
                settime()
                self.send2broker()
            except:
                pass
            time.sleep(3)