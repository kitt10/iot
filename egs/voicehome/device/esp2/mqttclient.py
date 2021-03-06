#!/usr/bin/env python
# coding: utf-8

import time
import machine
import ntptime
import utime
import usocket
from json import dumps, loads
from ntptime import settime
from umqtt.simple import MQTTClient
import config
from machine import Pin, I2C
from ds18b20 import tempSensorDS


class Client:

    def __init__(self):
        self.client = MQTTClient(config.MQTT['SENSOR_ID'], config.MQTT['SERVER'],
                                 config.MQTT['PORT'], config.MQTT['USER'], config.MQTT['PASSWD'])
        self.last_minute_sent = 99

        self.measure_temperature_now = False
        self.measure_temperature_now_last_msg = ''

        self.ESPled = Pin(2, Pin.OUT, value=1)

        self.light1 = machine.Pin(15, machine.Pin.OUT)

        try:
            self.tempSensorDS = tempSensorDS(pin_nb=0)
        except:
            print('can not init ds18b20')
            machine.reset()

    def send2broker_current_temperature(self):

        try:
            tempSensorDS = float(self.tempSensorDS.measure_temp())
        except:
            tempSensorDS = -9999
            pass

        if tempSensorDS < -55 or tempSensorDS > 125:
            status = 'error'
        else:
            status = 'ok'

        msg_structure_temperature = {'key': 'current_temperature',
                                     'sensor_id': config.MQTT['SENSOR_ID'],
                                     'timestamp': self.sync_time(),
                                     'value': float(tempSensorDS),
                                     'status': status,
                                     'location': config.MQTT['LOCATION'],
                                     'owner': config.MQTT['OWNER']}

        self.mqtt_msg(msg_structure_temperature,
                      config.MQTT['TOPIC_CURRENT_TEMPERATURE_COMMAND'])

        self.last_minute_sent = self.get_min()

    def send2broker(self):

        try:
            tempSensorDS = float(self.tempSensorDS.measure_temp())
        except:
            tempSensorDS = -9999
            pass
        print('tempSensorDS = ',tempSensorDS)
        if tempSensorDS < -55 or tempSensorDS > 125:
            status = 'error'
        else:
            status = 'ok'

        msg_structure_temperature = {'sensor_id': config.MQTT['SENSOR_ID'],
                                     'timestamp': self.sync_time(),
                                     'temperature_value': tempSensorDS,
                                     'status': status,
                                     'quantity': config.MQTT['QUANTITY_TEMPERATURE'],
                                     'location': config.MQTT['LOCATION'],
                                     'owner': config.MQTT['OWNER']}
        print(msg_structure_temperature)
        self.mqtt_msg(msg_structure_temperature,
                      config.MQTT['TOPIC_TEMPERATURE'])

        self.last_minute_sent = self.get_min()

    def sync_time(self):
        GMT = time.mktime(time.localtime()) + 3600
        (year, mon, mday, hour, minute, sec, wd, yd) = time.localtime(GMT)
        converted_time = (str(year) + '-' + "{:02d}".format(mon) + '-' + "{:02d}".format(
            mday) + ' ' + "{:02d}".format(hour) + ':' + "{:02d}".format(minute) + ':' + "{:02d}".format(sec))
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
                if msg['type'] == 'light':
                    if msg['ID'] in config.MQTT['LightsID']:
                        if msg['ID'] == 1:
                            if msg['set'] == 1:
                                self.light1.value(1)
                            elif msg['set'] == 0:
                                self.light1.value(0)
            elif 'command' in msg:
                if msg['command'] == 'measure_now':
                    if msg['quantity'] == 'temperature':
                        print('merim loool')
                        self.measure_temperature_now = True
                        measure_temperature_now_last_msg = msg
                        self.send2broker_current_temperature()

        self.client.set_callback(sub_cb)
        try:
            self.client.connect()
        except:
            print('Exception in connecting to MQTT')
            machine.reset()
        print(bytearray(config.MQTT['TOPIC_SUBSCRIBE_LIGHTS']))
        self.client.subscribe(bytearray(config.MQTT['TOPIC_SUBSCRIBE_LIGHTS']))
        self.client.subscribe(
            bytearray(config.MQTT['TOPIC_SUBSCRIBE_COMMAND']))
        print("Connected to %s, subscribed to %s topic" %
              (config.MQTT['SERVER'], config.MQTT['TOPIC_SUBSCRIBE_LIGHTS']))

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
