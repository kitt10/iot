#!/usr/bin/env python
# coding: utf-8

import time
import machine
import usocket
import os
from json import dumps, loads
from ntptime import settime
from umqtt.simple import MQTTClient
import config
import tsl2591
from machine import Pin, I2C
from bme280 import BME280
from ds18b20 import tempSensorDS

import ubinascii
import machine
import micropython

class Client:
    
    def __init__(self):
        self.client = MQTTClient(config.MQTT['SENSOR_ID'], config.MQTT['SERVER'], config.MQTT['PORT'], config.MQTT['USER'], config.MQTT['PASSWD'])
        self.last_minute_sent = 99

        self.tsl = tsl2591.Tsl2591(scl_pin_nb=5, sda_pin_nb=4)
        self.led = Pin(2, Pin.OUT, value=1)
        self.state = 0

        self.tempSensorDS = tempSensorDS(pin_nb=0)


        # self.i2c_bme = I2C(scl=Pin(14, Pin.IN), sda=Pin(12, Pin.IN))
        # self.bme = BME280(i2c=self.i2c_bme)
          
    def send2broker(self):
        illuminance = self.tsl.sample()
        # pressure = self.bme.pressure
        # print(pressure)
        # temperature = self.bme.temperature
        # print(temperature)
        # humidity = self.bme.humidity
        # print(humidity)
        tempSensorDS = self.tempSensorDS.measure_temp()
        if illuminance == -1:
            status = 'sensor_error'
        else:
            status = 'ok'    
        structure = {'sensor_id': config.MQTT['SENSOR_ID'], \
                'timestamp': self.sync_time(), \
                'illuminance_value': float(illuminance), \
                # 'pressure_value': float(pressure), \
                # 'temperature_value': float(temperature), \
                # 'humidity_value': float(humidity), \
                'tempSensorDS_value': float(tempSensorDS), \
                'status': status, \
                'quantity': config.MQTT['QUANTITY'], \
                'location': config.MQTT['LOCATION'], \
                'owner': config.MQTT['OWNER']}
        self.mqtt_msg(structure)

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
        print(bytearray(config.MQTT['TOPIC_SUBSCRIBE']))
        self.client.subscribe(bytearray(config.MQTT['TOPIC_SUBSCRIBE']))
        print("Connected to %s, subscribed to %s topic" % (config.MQTT['SERVER'], config.MQTT['TOPIC_SUBSCRIBE']))

    def subscribe(self):
        print("subscribe")
        self.client.check_msg()
    
    def mqtt_msg(self, structure):
        try:
            self.client.publish(config.MQTT['TOPIC_SENSOR'], dumps(structure))
            self.last_minute_sent = self.get_min()
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