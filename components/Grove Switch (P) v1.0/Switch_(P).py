from machine import Pin
import time

switch_pin = Pin(0, Pin.IN)

while True:

    switch_state = switch_pin.value()

    if switch_state == 0:
        print("on")
    else:
        print("off")

    time.sleep(0.1)
#pinout D3