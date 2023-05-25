import machine
import time

pin = machine.Pin(4, machine.Pin.OUT)

def turn_on():
    pin.on()

def turn_off():
    pin.off()

while True:
    turn_on()
    time.sleep(5)
    turn_off()
    time.sleep(1)
