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

class Client:
    
    def __init__(self):
        self.client = MQTTClient(config.MQTT['SENSOR_1_ID'], config.MQTT['SERVER'], config.MQTT['PORT'], config.MQTT['USER'], config.MQTT['PASSWD'], config.MQTT['KEEPALIVE'])
        self.window = machine.Pin(config.GPIO['MAGNET_1'], machine.Pin.IN, machine.Pin.PULL_UP)
        self.door = machine.Pin(config.GPIO['MAGNET_2'], machine.Pin.IN, machine.Pin.PULL_UP)    
          
    def send2broker(self):
        while True:
            window_state_1 = self.window.value()
            door_state_1 = self.door.value()
            time.sleep_ms(500)
            window_state_2 = self.window.value()
            door_state_2 = self.door.value()

            if window_state_1 and not window_state_2:
                functions.external_led_1_blick(1,100)
                structure = {'sensor_id': config.MQTT['SENSOR_1_ID'], \
                        'timestamp': self.sync_time(), \
                        'value': 0, \
                        'status': 'ok', \
                        'quantity': config.MQTT['QUANTITY_2'], \
                        'location': config.MQTT['LOCATION'], \
                        'owner': config.MQTT['OWNER']}
                self.mqtt_msg(config.MQTT['TOPIC_2'], structure)
            elif not window_state_1 and window_state_2:
                functions.external_led_1_blick(1,100)
                structure = {'sensor_id': config.MQTT['SENSOR_1_ID'], \
                        'timestamp': self.sync_time(), \
                        'value': 1, \
                        'status': 'ok', \
                        'quantity': config.MQTT['QUANTITY_2'], \
                        'location': config.MQTT['LOCATION'], \
                        'owner': config.MQTT['OWNER']}
                self.mqtt_msg(config.MQTT['TOPIC_2'], structure)
            elif door_state_1 and not door_state_2:
                functions.external_led_2_blick(1,100)
                structure = {'sensor_id': config.MQTT['SENSOR_2_ID'], \
                        'timestamp': self.sync_time(), \
                        'value': 0, \
                        'status': 'ok', \
                        'quantity': config.MQTT['QUANTITY_1'], \
                        'location': config.MQTT['LOCATION'], \
                        'owner': config.MQTT['OWNER']}
                self.mqtt_msg(config.MQTT['TOPIC_1'], structure)
            elif not door_state_1 and door_state_2:
                functions.external_led_2_blick(1,100)
                structure = {'sensor_id': config.MQTT['SENSOR_2_ID'], \
                        'timestamp': self.sync_time(), \
                        'value': 1, \
                        'status': 'ok', \
                        'quantity': config.MQTT['QUANTITY_1'], \
                        'location': config.MQTT['LOCATION'], \
                        'owner': config.MQTT['OWNER']}
                self.mqtt_msg(config.MQTT['TOPIC_1'], structure)
                break
            time.sleep_ms(10)

    def sync_time(self):
        GMT = time.mktime(time.localtime()) + 3600
        (year, mon, mday, hour, minute, sec, wd, yd) = time.localtime(GMT)          
        converted_time = (str(year) + '-' + "{:02d}".format(mon) + '-' + "{:02d}".format(mday) + ' ' + "{:02d}".format(hour) + ':' + "{:02d}".format(minute) + ':' + "{:02d}".format(sec))
        return converted_time
    
    def mqtt_msg(self, topic, structure):
        self.client.connect()
        self.client.publish(topic, dumps(structure))
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
            time.sleep_ms(10)