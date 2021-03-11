#!/usr/bin/env python
# coding: utf-8


import machine
import utime
import socket
import time
import struct

from json import dumps, loads
from umqtt.simple import MQTTClient
import config
from machine import Pin, I2C
from bme280 import BME280


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
            self.i2c_bme = I2C(scl=Pin(14, Pin.IN), sda=Pin(12, Pin.IN))
            self.bme = BME280(i2c=self.i2c_bme)
        except:
            print('can not init bme280')
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

        # illuminance = self.tsl.sample()
        try:
            temperature,pressure,humidity = self.bme.values
        except:
            pressure = -9999
            temperature = -9999
            humidity = -9999
            pass

        if pressure < 300 or pressure > 1100:
            state = 'error'
        else:
            state = 'ok'

        msg['sensor_id']= config.MQTT['SENSOR_ID']
        msg['timestamp']= self.sync_time()
        msg['pressure_value']= pressure
        msg['state']= state
        msg['quantity_units']= config.MQTT['QUANTITY_UNITS_PRESSURE']
        msg['quantity_type']= config.MQTT['QUANTITY_TYPE_PRESSURE']
        msg['location']= config.MQTT['LOCATION']
        msg['owner']= config.MQTT['OWNER']

        print(msg)
        self.mqtt_msg(msg, config.MQTT['TOPIC_PRESSURE'])
        self.mqtt_msg(msg,
                      config.MQTT['TOPIC_MEASURE_COMMAND'])


        if temperature < -40 or temperature > 85:
            state = 'error'
        else:
            state = 'ok'

        msg['sensor_id']= config.MQTT['SENSOR_ID']
        msg['timestamp']= self.sync_time()
        msg['temperature_value']= temperature
        msg['state']= state
        msg['quantity_units']= config.MQTT['QUANTITY_UNITS_TEMPERATURE']
        msg['quantity_type']= config.MQTT['QUANTITY_TYPE_TEMPERATURE']
        msg['location']= config.MQTT['LOCATION']
        msg['owner']= config.MQTT['OWNER']

        print(msg)
        self.mqtt_msg(msg, config.MQTT['TOPIC_TEMPERATURE'])
        self.mqtt_msg(msg,
                      config.MQTT['TOPIC_MEASURE_COMMAND'])


        if humidity <= 0 or humidity > 100:
            state = 'error'
        else:
            state = 'ok'

        msg['sensor_id']= config.MQTT['SENSOR_ID']
        msg['timestamp']= self.sync_time()
        msg['humidity_value']= pressure
        msg['state']= state
        msg['quantity_units']= config.MQTT['QUANTITY_UNITS_HUMIDITY']
        msg['quantity_type']= config.MQTT['QUANTITY_TYPE_HUMIDITY']
        msg['location']= config.MQTT['LOCATION']
        msg['owner']= config.MQTT['OWNER']

        print(msg)
        self.mqtt_msg(msg, config.MQTT['TOPIC_HUMIDITY'])
        self.mqtt_msg(msg,
                      config.MQTT['TOPIC_MEASURE_COMMAND'])

        # self.last_minute_sent = self.get_min()

    def send2broker(self):

        # illuminance = self.tsl.sample()
        try:
            temperature,pressure,humidity = self.bme.values
        except:
            pressure = -9999
            temperature = -9999
            humidity = -9999
            pass

        if pressure < 300 or pressure > 1100:
            state = 'error'
        else:
            state = 'ok'

        msg_structure_pressure = {'sensor_id': config.MQTT['SENSOR_ID'],
                                  'timestamp': self.sync_time(),
                                  'pressure_value': pressure,
                                  'state': state,
                                  'quantity_units': config.MQTT['QUANTITY_UNITS_PRESSURE'],
                                  'quantity_type': config.MQTT['QUANTITY_TYPE_PRESSURE'],
                                  'location': config.MQTT['LOCATION'],
                                  'owner': config.MQTT['OWNER']}

        if temperature < -40 or temperature > 85:
            state = 'error'
        else:
            state = 'ok'

        msg_structure_temperature = {'sensor_id': config.MQTT['SENSOR_ID'],
                                      'timestamp': self.sync_time(),
                                      'temperature_value': temperature,
                                      'state': state,
                                      'quantity_units': config.MQTT['QUANTITY_UNITS_TEMPERATURE'],
                                      'quantity_type': config.MQTT['QUANTITY_TYPE_TEMPERATURE'],
                                      'location': config.MQTT['LOCATION'],
                                      'owner': config.MQTT['OWNER']}

        if humidity <= 0 or humidity > 100:
            state = 'error'
        else:
            state = 'ok'

        msg_structure_humidity = {'sensor_id': config.MQTT['SENSOR_ID'],
                                  'timestamp': self.sync_time(),
                                  'humidity_value': pressure,
                                  'state': state,
                                  'quantity_units': config.MQTT['QUANTITY_UNITS_HUMIDITY'],
                                  'quantity_type': config.MQTT['QUANTITY_TYPE_HUMIDITY'],
                                  'location': config.MQTT['LOCATION'],
                                  'owner': config.MQTT['OWNER']}
        print(msg_structure_pressure)
        print(msg_structure_temperature)
        print(msg_structure_humidity)
        # self.mqtt_msg(msg_structure_illuminance, config.MQTT['TOPIC_ILLUMINANCE'])
        self.mqtt_msg(msg_structure_pressure, config.MQTT['TOPIC_PRESSURE'])
        self.mqtt_msg(msg_structure_temperature, config.MQTT['TOPIC_TEMPERATURE'])
        self.mqtt_msg(msg_structure_humidity, config.MQTT['TOPIC_HUMIDITY'])

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
                state = 'error'
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
