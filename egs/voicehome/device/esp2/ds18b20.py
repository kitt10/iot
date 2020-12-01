from machine import Pin
from onewire import OneWire
from ds18x20 import DS18X20
from time import sleep

class tempSensorDS:

    def __init__(self, pin_nb):
        self.pin = Pin(pin_nb, Pin.IN)
        self.ow = DS18X20(OneWire(self.pin))
        self.ds_sensor = self.scan()

    def scan(self):
        try:
            return self.ow.scan()[0]
        except IndexError:
            print('ERR: No DS sensors found.')
            exit(0)

    def measure_temp(self, delay=0.75):
        self.ow.convert_temp()
        sleep(delay)
        return self.ow.read_temp(self.ds_sensor)