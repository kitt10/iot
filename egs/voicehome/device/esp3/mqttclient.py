#!/usr/bin/env python
# coding: utf-8

import time
import machine
import ntptime
import utime
import usocket

import socket
import network
import utime
import socket
import time
import struct

from json import dumps, loads
from umqtt.simple import MQTTClient
import config
from machine import Pin, I2C
import tsl2591


class Client:

    def __init__(self):
        self.client = MQTTClient(config.MQTT['SENSOR_ID'], config.MQTT['SERVER'],
                                 config.MQTT['PORT'], config.MQTT['USER'], config.MQTT['PASSWD'],
                                 config.MQTT['KEEPALIVE'])
        self.last_minute_sent = 99

        # self.measure_temperature_now = False
        # self.measure_temperature_now_last_msg = ''

        self.ESPled = Pin(2, Pin.OUT, value=1)

        # self.light1 = machine.Pin(15, machine.Pin.OUT)
        # msg_structure_state = {'ID': config.MQTT['LightsID'][0],
        #                        'type': 'light',
        #                        'state': self.light1.value()
        #                        }
        # print(msg_structure_state)
        # self.mqtt_msg(msg_structure_state,
        #               config.MQTT['TOPIC_LIGHTS_STATE'])


        # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
        self.NTP_DELTA = 3155673600

        self.host = "pool.ntp.org"

        self.num_subscribe_error = 0

        try:
            self.tsl = tsl2591.Tsl2591(scl_pin_nb=5, sda_pin_nb=4)
        except:
            print('can not init tsl2591')
            machine.reset()

        try:
            print("Get NTP Time")
            # set the RTC using time from ntp
            self.settime()
            print("Display RTC Time")
            # print out RTC datetime
            print(machine.RTC().datetime())
            print("utime time")
            print(utime.localtime())
        except:
            print('Exception in __init__ ntptime')
            machine.reset()

    def getntptime(self):
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1b
        addr = socket.getaddrinfo(self.host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
        s.close()

        val = struct.unpack("!I", msg[40:44])[0]
        return val - self.NTP_DELTA

    def settime(self):

        t = self.getntptime()
        tm = utime.localtime(t)
        tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        machine.RTC().datetime(tm)

    def send2broker_measure_now(self, msg):
        
        state = 'ok'
        try:
            illuminance = float(self.tsl.sample())
        except:
            illuminance=-1
            pass
        if illuminance < 0:
            state = 'error'


        print('illuminance = ', illuminance)
        msg['sensor_id']= config.MQTT['SENSOR_ID']
        msg['timestamp']= self.sync_time()
        msg['illuminance_value']= illuminance
        msg['state']= state
        msg['quantity_units']= config.MQTT['QUANTITY_UNITS_ILLUMINANCE']
        msg['quantity_type']= config.MQTT['QUANTITY_TYPE_ILLUMINANCE']
        msg['location']= config.MQTT['LOCATION']
        msg['owner']= config.MQTT['OWNER']


        print(msg)
        self.mqtt_msg(msg,
                      config.MQTT['TOPIC_MEASURE_COMMAND'])
        self.mqtt_msg(msg, config.MQTT['TOPIC_ILLUMINANCE'])

        # self.last_minute_sent = self.get_min()
        

    def send2broker(self):

        state = 'ok'
        try:
            illuminance = float(self.tsl.sample())
        except:
            illuminance=-1
            pass
        if illuminance < 0:
            state = 'error'


        print('illuminance = ', illuminance)
        msg_structure_illuminance = {'sensor_id': config.MQTT['SENSOR_ID'], 
            'timestamp': self.sync_time(), 
            'illuminance_value': illuminance, 
            'state': state, 
            'quantity_units': config.MQTT['QUANTITY_UNITS_ILLUMINANCE'],
            'quantity_type': config.MQTT['QUANTITY_TYPE_ILLUMINANCE'],
            'location': config.MQTT['LOCATION'], 
            'owner': config.MQTT['OWNER']}


        print(msg_structure_illuminance)

        self.mqtt_msg(msg_structure_illuminance, config.MQTT['TOPIC_ILLUMINANCE'])

        self.last_minute_sent = self.get_min()

    def sync_time(self):
        GMT = time.mktime(time.localtime()) + 7200
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
                    if msg['ID'] == config.MQTT['ESP_ID']:
                        self.ESPled.value(msg['set'])
                        msg_structure_state = {'ID': msg['ID'],
                                               'type': msg['type'],
                                               'state': msg['set']
                                               }
                        print(msg_structure_state)
                        self.mqtt_msg(msg_structure_state,
                                      config.MQTT['TOPIC_LIGHTS_STATE'])
                # if msg['type'] == 'light':
                #     if msg['ID'] in config.MQTT['LightsID']:
                #         if msg['ID'] == 1:
                #             self.light1.value(msg['set'])
                #             msg_structure_state = {'ID': msg['ID'],
                #                                    'type': msg['type'],
                #                                    'state': msg['set']
                #                                    }
                #             print(msg_structure_state)
                #             self.mqtt_msg(msg_structure_state,
                #                           config.MQTT['TOPIC_LIGHTS_STATE'])

            elif topic == bytearray(config.MQTT['TOPIC_SUBSCRIBE_LIGHTS_STATE']):
                state = 'error'
                if msg['type'] == 'ESP_onboard':
                    if msg['ID'] == config.MQTT['ESP_ID']:
                        state = self.ESPled.value()
                        msg_structure_state = {'ID': msg['ID'],
                                               'type': msg['type'],
                                               'state': state
                                               }
                        print(msg_structure_state)
                        self.mqtt_msg(msg_structure_state,
                                      config.MQTT['TOPIC_LIGHTS_STATE'])
                # if msg['type'] == 'light':
                #     if msg['ID'] in config.MQTT['LightsID']:
                #         if msg['ID'] == 1:
                #             state = self.light1.value()
                #             msg_structure_state = {'ID': msg['ID'],
                #                                    'type': msg['type'],
                #                                    'state': state
                #                                    }
                #             print(msg_structure_state)
                #             self.mqtt_msg(msg_structure_state,
                #                           config.MQTT['TOPIC_LIGHTS_STATE'])



            elif topic == bytearray(config.MQTT['TOPIC_MEASURE_COMMAND']):
                if 'command' in msg:
                    if msg['command'] == 'measure_now':
                        if 'timestamp' not in msg:
                            if msg['sensor_ID'] == config.MQTT['SENSOR_ID']:
                                self.send2broker_measure_now(msg)

        self.client.set_callback(sub_cb)
        try:
            self.client.connect()
        except:
            print('Exception in connecting to MQTT')
            machine.reset()
        print(bytearray(config.MQTT['TOPIC_SUBSCRIBE_LIGHTS']))
        self.client.subscribe(bytearray(config.MQTT['TOPIC_SUBSCRIBE_LIGHTS']))
        self.client.subscribe(
            bytearray(config.MQTT['TOPIC_MEASURE_COMMAND']))
        self.client.subscribe(
            bytearray(config.MQTT['TOPIC_SUBSCRIBE_LIGHTS_STATE']))
        print("Connected to %s, subscribed to %s topic" %
              (config.MQTT['SERVER'], config.MQTT['TOPIC_SUBSCRIBE_LIGHTS']))

    def subscribe(self):
        print("subscribe")
        try:
            self.client.check_msg()
            self.num_subscribe_error = 0
        except:
            if self.num_subscribe_error > 5:  # check if it is just unique error
                print("Subscribe exception occurred")
                print('num_subscribe_error = ' + str(self.num_subscribe_error))
                machine.reset()
            else:
                print("Subscribe exception occurred")
                print('num_subscribe_error = ' + str(self.num_subscribe_error))
                self.num_subscribe_error = self.num_subscribe_error + 1
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
                print("Get NTP Time")
                # set the RTC using time from ntp
                self.settime()
                print("Display RTC Time")
                # print out RTC datetime
                print(machine.RTC().datetime())
                print("utime time")
                print(utime.localtime())
            except:
                print('Exception in ntptime')
                # machine.reset()
                pass
            self.send2broker()
        except:
            print("Exception in publish")
            machine.reset()
