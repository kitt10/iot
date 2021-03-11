#!/usr/bin/env python
# coding: utf-8

import time
import usocket
import machine
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

        try:
            self.i2c_bme = I2C(scl=Pin(14, Pin.IN), sda=Pin(12, Pin.IN))
            self.bme = BME280(i2c=self.i2c_bme)
        except:
            print('can not init bme280')
            machine.reset()

    def send2broker(self):
        # illuminance = self.tsl.sample()
        try:
            pressure = float(self.bme.pressure)
        except:
            pressure = -9999
            pass
        print(pressure)
        try:
            temperature = float(self.bme.temperature)
        except:
            temperature = -9999
            pass
        print(temperature)
        try:
            humidity = float(self.bme.humidity)
        except:
            humidity = -9999
            pass
        print(humidity)

        if pressure < 300 or pressure > 1100:
            status = 'error'
        else:
            status = 'ok'

        msg_structure_pressure = {'sensor_id': config.MQTT['SENSOR_ID'], \
            'timestamp': self.sync_time(), \
            'pressure_value': pressure, \
            'status': status, \
            'quantity': config.MQTT['QUANTITY_PRESSURE'], \
            'location': config.MQTT['LOCATION'], \
            'owner': config.MQTT['OWNER']}

        if temperature < -40 or temperature > 85:
            status = 'error'
        else:
            status = 'ok'

        msg_structure_temperature = {'sensor_id': config.MQTT['SENSOR_ID'], \
            'timestamp': self.sync_time(), \
            'temperature_value': temperature, \
            'status': status, \
            'quantity': config.MQTT['QUANTITY_TEMPERATURE'], \
            'location': config.MQTT['LOCATION'], \
            'owner': config.MQTT['OWNER']}

        if humidity <= 0 or humidity > 100:
            status = 'error'
        else:
            status = 'ok'

        msg_structure_humidity = {'sensor_id': config.MQTT['SENSOR_ID'], \
            'timestamp': self.sync_time(), \
            'humidity_value': humidity, \
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
            msg = loads(msg)
            if topic == bytearray(config.MQTT['TOPIC_SUBSCRIBE_LIGHTS']):
                if msg['type'] == 'ESP_onboard':
                    if msg['ID'] == config.MQTT['ESP_ID'] or msg['ID'] == 'all':
                        if msg['set'] == 1:
                            self.ESPled.value(0)
                        elif msg['set'] == 0:
                            self.ESPled.value(1)
                # if msg['type'] == 'light':
                #     if msg['ID'] in config.MQTT['LightsID']:
                #         if msg['ID'] == 1:
                #             if msg['set'] == 1:
                #                 self.light1.value(1)
                #             elif msg['set'] == 0:
                #                 self.light1.value(0)

        self.client.set_callback(sub_cb)
        try:
            self.client.connect()
        except:
            print('Exception in connecting to MQTT')
            machine.reset()
        print(bytearray(config.MQTT['TOPIC_SUBSCRIBE_LED']))
        self.client.subscribe(bytearray(config.MQTT['TOPIC_SUBSCRIBE_LED']))
        print("Connected to %s, subscribed to %s topic" % (config.MQTT['SERVER'], config.MQTT['TOPIC_SUBSCRIBE_LED']))

    def subscribe(self):
        print("subscribe")
        try:
            self.client.check_msg()
        except:
            print("Subscribe exception occurred")
            machine.reset()
            pass

    def mqtt_msg(self, msg_structure, topic):
        try:
            self.client.publish(topic, dumps(msg_structure))
        except:
            print("mqtt_msg error")
            machine.reset()
            pass


    def publish(self):
        print("publish")
        try:
            try:
                # a = usocket.getaddrinfo('8.8.8.8',80)[0][-1]
                settime()
            except:
                print('Exception in usocket get www.google.com')
                machine.reset()
            self.send2broker()
        except:
            print("Exception in publish")
            pass