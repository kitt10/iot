#!/usr/bin/env python
# coding: utf-8

import time
import usocket
from json import dumps, loads
from ntptime import settime
from umqtt.simple import MQTTClient
import config
from machine import Pin, I2C
from ds18b20 import tempSensorDS

class Client:
    
    def __init__(self):
        self.client = MQTTClient(config.MQTT['SENSOR_ID'], config.MQTT['SERVER'], config.MQTT['PORT'], config.MQTT['USER'], config.MQTT['PASSWD'])
        self.last_minute_sent = 99

        self.led = Pin(2, Pin.OUT, value=1)
        self.state = 0

        self.tempSensorDS = tempSensorDS(pin_nb=0)
          
    def send2broker(self):
        
        tempSensorDS = self.tempSensorDS.measure_temp()

        # if illuminance == -1:
        #     status = 'sensor_error'
        # else:
        status = 'ok'

        msg_structure_temperature = {'sensor_id': config.MQTT['SENSOR_ID'], \
            'timestamp': self.sync_time(), \
            'temperature_value': float(tempSensorDS), \
            'status': status, \
            'quantity': config.MQTT['QUANTITY_TEMPERATURE'], \
            'location': config.MQTT['LOCATION'], \
            'owner': config.MQTT['OWNER']}


        self.mqtt_msg(msg_structure_temperature, config.MQTT['TOPIC_TEMPERATURE'])

        self.last_minute_sent = self.get_min()

    def sync_time(self):
        GMT = time.mktime(time.localtime()) + 3600
        (year, mon, mday, hour, minute, sec, wd, yd) = time.localtime(GMT)          
        converted_time = (str(year) + '-' + "{:02d}".format(mon) + '-' + "{:02d}".format(mday) + ' ' + "{:02d}".format(hour) + ':' + "{:02d}".format(minute) + ':' + "{:02d}".format(sec))
        return converted_time
    
    def get_sec(self):
        return time.localtime()[5]

    def get_min(self):
        return time.localtime()[4]    

    def connect(self):
        def sub_cb(topic, msg):
            print((topic, msg))
            msg1 = loads(msg)
            if msg1['set'] == 1:
                self.led.value(0)
                self.state = 1
                print("1")
            elif msg1['set'] == 0:
                self.led.value(1)
                self.state = 0
                print("0")
            elif msg == b"toggle":
                # LED is inversed, so setting it to current state
                # value will make it toggle
                self.led.value(self.state)
                self.state = 1 - self.state
                print("toggle")
        self.client.set_callback(sub_cb)
        self.client.connect()
        print(bytearray(config.MQTT['TOPIC_SUBSCRIBE_LED']))
        self.client.subscribe(bytearray(config.MQTT['TOPIC_SUBSCRIBE_LED']))
        print("Connected to %s, subscribed to %s topic" % (config.MQTT['SERVER'], config.MQTT['TOPIC_SUBSCRIBE_LED']))

    def subscribe(self):
        print("subscribe")
        self.client.check_msg()
    
    def mqtt_msg(self, msg_structure, topic):
        try:
            self.client.publish(topic, dumps(msg_structure))
        except:
            print("mqtt_msg error")
            pass
        
        
    def publish(self):
        print("publish")
        try:
            a = usocket.getaddrinfo('www.google.com',80)[0][-1]
            settime()
            self.send2broker()
        except:
            print("Exception in publish")
            pass