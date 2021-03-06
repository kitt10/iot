#!/usr/bin/env python
# coding: utf-8

import time
import usocket
from json import dumps, loads
from ntptime import settime
from umqtt.simple import MQTTClient
import config
# import tsl2591
from machine import Pin, I2C
from bme280 import BME280

class Client:
    
    def __init__(self):
        self.client = MQTTClient(config.MQTT['SENSOR_ID'], config.MQTT['SERVER'], config.MQTT['PORT'], config.MQTT['USER'], config.MQTT['PASSWD'])
        self.last_minute_sent = 99

        # self.tsl = tsl2591.Tsl2591(scl_pin_nb=5, sda_pin_nb=4)
        self.led = Pin(2, Pin.OUT, value=1)
        self.state = 0


        self.i2c_bme = I2C(scl=Pin(14, Pin.IN), sda=Pin(12, Pin.IN))
        self.bme = BME280(i2c=self.i2c_bme)
          
    def send2broker(self):
        # illuminance = self.tsl.sample()
        pressure = self.bme.pressure
        print(pressure)
        temperature = self.bme.temperature
        print(temperature)
        humidity = self.bme.humidity
        print(humidity)
        # if illuminance == -1:
        #     status = 'sensor_error'
        # else:
        status = 'ok'    
        # msg_structure_illuminance = {'sensor_id': config.MQTT['SENSOR_ID'], \
        #     'timestamp': self.sync_time(), \
        #     'illuminance_value': float(illuminance), \
        #     'status': status, \
        #     'quantity': config.MQTT['QUANTITY_ILLUMINANCE'], \
        #     'location': config.MQTT['LOCATION'], \
        #     'owner': config.MQTT['OWNER']}

        msg_structure_pressure = {'sensor_id': config.MQTT['SENSOR_ID'], \
            'timestamp': self.sync_time(), \
            'pressure_value': float(pressure), \
            'status': status, \
            'quantity': config.MQTT['QUANTITY_PRESSURE'], \
            'location': config.MQTT['LOCATION'], \
            'owner': config.MQTT['OWNER']}

        msg_structure_temperature = {'sensor_id': config.MQTT['SENSOR_ID'], \
            'timestamp': self.sync_time(), \
            'temperature_value': float(temperature), \
            'status': status, \
            'quantity': config.MQTT['QUANTITY_TEMPERATURE'], \
            'location': config.MQTT['LOCATION'], \
            'owner': config.MQTT['OWNER']}
        
        msg_structure_humidity = {'sensor_id': config.MQTT['SENSOR_ID'], \
            'timestamp': self.sync_time(), \
            'humidity_value': float(humidity), \
            'status': status, \
            'quantity': config.MQTT['QUANTITY_HUMIDITY'], \
            'location': config.MQTT['LOCATION'], \
            'owner': config.MQTT['OWNER']}



        # self.mqtt_msg(msg_structure_illuminance, config.MQTT['TOPIC_ILLUMINANCE'])
        self.mqtt_msg(msg_structure_pressure, config.MQTT['TOPIC_PRESSURE'])
        self.mqtt_msg(msg_structure_temperature, config.MQTT['TOPIC_TEMPERATURE'])
        self.mqtt_msg(msg_structure_humidity, config.MQTT['TOPIC_HUMIDITY'])

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