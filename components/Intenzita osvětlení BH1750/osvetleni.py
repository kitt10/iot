from machine import Pin
import time

light_pin = Pin(4, Pin.IN) #SDA to D2

def read_light_intensity():
    light_intensity = light_pin.value()
    return light_intensity

while True:
    intensity = read_light_intensity()
    if intensity == 0:
        print("Light detected")
    else:
        print("Light not detected")
    time.sleep(1)