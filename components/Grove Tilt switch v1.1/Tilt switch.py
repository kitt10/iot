import machine
import time

switch_pin = machine.Pin(4, machine.Pin.IN)

while True:
    if switch_pin.value() == 1:
        print("on")
       
    else:
        print("off")
    time.sleep(0.1)