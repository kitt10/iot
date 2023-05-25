from machine import Pin
import time

button_pin = Pin(0, Pin.IN)
# pin D3
while True:

    button_state = button_pin.value()

    if button_state == 0:
        print("off")
    else: print("on")

    time.sleep(0.1)