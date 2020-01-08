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
from temphumid import TempHumidSensor

class Client:
    
    def __init__(self):
        self.client = MQTTClient(config.MQTT['SENSOR_1_ID'], config.MQTT['SERVER'], config.MQTT['PORT'], config.MQTT['USER'], config.MQTT['PASSWD'], config.MQTT['KEEPALIVE'])
        self.ths = TempHumidSensor()
        self.last_minute_sent = 99 
          
    def send2broker(self):
        while True:
            if self.get_sec() in range(30,33):
                if self.last_minute_sent == self.get_min():
                    break
                values = self.ths.measure()
                if values[0] == -100:
                    status_1 = 'ds18b20_inside_error'
                else:
                    status_1 = 'ok'    
                structure_1 = {'sensor_id': config.MQTT['SENSOR_1_ID'], \
                        'timestamp': self.sync_time(), \
                        'value': float(values[0]), \
                        'status': status_1, \
                        'quantity': config.MQTT['QUANTITY_1'], \
                        'location': config.MQTT['LOCATION_1'], \
                        'owner': config.MQTT['OWNER']}
                if values[1] == -100:
                    status_2 = 'ds18b20_outside_error'
                else:
                    status_2 = 'ok'    
                structure_2 = {'sensor_id': config.MQTT['SENSOR_2_ID'], \
                        'timestamp': self.sync_time(), \
                        'value': float(values[1]), \
                        'status': status_2, \
                        'quantity': config.MQTT['QUANTITY_1'], \
                        'location': config.MQTT['LOCATION_2'], \
                        'owner': config.MQTT['OWNER']}
                if values[2] == -1:
                    status_3 = 'dht11_error'
                else:  
                    status_3 = 'ok'    
                structure_3 = {'sensor_id': config.MQTT['SENSOR_3_ID'], \
                        'timestamp': self.sync_time(), \
                        'value': float(values[2]), \
                        'status': status_3, \
                        'quantity': config.MQTT['QUANTITY_2'], \
                        'location': config.MQTT['LOCATION_1'], \
                        'owner': config.MQTT['OWNER']}      
                self.mqtt_msg(structure_1, structure_2, structure_3)
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
    
    def mqtt_msg(self, structure_1, structure_2, structure_3):
        self.client.connect()
        self.client.publish(config.MQTT['TEMPERATURE_IN_TOPIC'], dumps(structure_1))
        self.client.publish(config.MQTT['TEMPERATURE_OUT_TOPIC'], dumps(structure_2))
        self.client.publish(config.MQTT['HUMIDITY_TOPIC'], dumps(structure_3))
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