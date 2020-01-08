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
import tsl2591

class Client:
    
    def __init__(self):
        self.client = MQTTClient(config.MQTT['SENSOR_ID'], config.MQTT['SERVER'], config.MQTT['PORT'], config.MQTT['USER'], config.MQTT['PASSWD'], config.MQTT['KEEPALIVE'])
        self.tsl = tsl2591.Tsl2591()
        self.last_minute_sent = 99
          
    def send2broker(self):
        while True:
            if self.get_sec() in range(30,33):
                if self.last_minute_sent == self.get_min():
                    break
                illuminance = self.tsl.measure()
                if illuminance == -1:
                    status = 'sensor_error'
                else:
                    status = 'ok'    
                structure = {'sensor_id': config.MQTT['SENSOR_ID'], \
                        'timestamp': self.sync_time(), \
                        'value': float(illuminance), \
                        'status': status, \
                        'quantity': config.MQTT['QUANTITY'], \
                        'location': config.MQTT['LOCATION'], \
                        'owner': config.MQTT['OWNER']}
                self.mqtt_msg(structure)
                time.sleep_ms(1500)    
                break
            time.sleep_ms(10)

    def sync_time(self):
        GMT = time.mktime(time.localtime()) + 3600
        (year, mon, mday, hour, minute, sec, wd, yd) = time.localtime(GMT)          
        converted_time = (str(year) + '-' + "{:02d}".format(mon) + '-' + "{:02d}".format(mday) + ' ' + "{:02d}".format(hour) + ':' + "{:02d}".format(minute) + ':' + "{:02d}".format(sec))
        return converted_time
    
    def get_sec(self):
        return time.localtime()[5]

    def get_min(self):
        return time.localtime()[4]    
    
    def mqtt_msg(self, structure):
        self.client.connect()
        self.client.publish(config.MQTT['ILLUMINANCE_TOPIC'], dumps(structure))
        self.last_minute_sent = self.get_min()
        self.client.disconnect()
        
    def publish(self, period):
        while True:
            try:
                if gc.mem_free() < 20000:
                    gc.collect()
                a = usocket.getaddrinfo('www.google.com',80)[0][-1]
                settime()
                self.send2broker()
            except:
                pass
            time.sleep(period)