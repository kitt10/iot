#!/usr/bin/env python
# coding: utf-8

import time
import machine
import onewire
import ds18x20
import dht
import config

class TempHumidSensor:

    def __init__(self):
        ds18b20_inside = machine.Pin(config.GPIO['DS18B20_INSIDE'], machine.Pin.IN)
        ds18b20_outside = machine.Pin(config.GPIO['DS18B20_OUTSIDE'], machine.Pin.IN)
        self.ds_inside = ds18x20.DS18X20(onewire.OneWire(ds18b20_inside))
        self.ds_outside = ds18x20.DS18X20(onewire.OneWire(ds18b20_outside))
        self.humid = dht.DHT11(machine.Pin(config.GPIO['DHT11']))
        try:
            self.device_inside = self.ds_inside.scan().pop()
        except IndexError:
            pass
        try:
            self.device_outside = self.ds_outside.scan().pop()
        except IndexError:
            pass

    def measure(self):
        try:
            self.ds_inside.convert_temp()
            temperature_inside = '%.2f' % round(self.ds_inside.read_temp(self.device_inside),2)
        except:
            temperature_inside = -100

        try:
            self.ds_outside.convert_temp()
            temperature_outside = '%.2f' % round(self.ds_outside.read_temp(self.device_outside),2)
        except:
            temperature_outside = -100 

        time.sleep(2)
        try:
            self.humid.measure()
            humidity_inside = self.humid.humidity()
        except OSError:
            humidity_inside = -1
        
        return [temperature_inside, temperature_outside, humidity_inside]