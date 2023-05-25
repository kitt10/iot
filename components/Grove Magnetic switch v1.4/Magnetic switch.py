import machine
import time

switch_pin = machine.Pin(4, machine.Pin.IN)

while True:
    if switch_pin.value() == 0:
        print("off")
   
    else:
        print("on")
    time.sleep(0.1)