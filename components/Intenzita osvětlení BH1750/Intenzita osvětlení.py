
from machine import Pin
import time
sda_pin = Pin(4, Pin.OUT)
scl_pin = Pin(5, Pin.OUT)
def start_transmission():
    sda_pin.value(1)
    scl_pin.value(1)
    sda_pin.value(0)
    scl_pin.value(0)
def stop_transmission():
    scl_pin.value(0)
    sda_pin.value(0)
    scl_pin.value(1)
    sda_pin.value(1)
def read_light_intensity():
    start_transmission()
    scl_pin.value(1)
    time.sleep_ms(180)
    scl_pin.value(0)
    stop_transmission()
    return sda_pin.value()
while True:
    light_level = read_light_intensity()
    if light_level == 1:
        print("Light detected")
    else:
        print("Light not detected")
    time.sleep(1)