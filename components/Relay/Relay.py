import machine
import time

relay_pin = machine.Pin(4, machine.Pin.OUT) 


def turn_relay_on():
    relay_pin.value(1) 

def turn_relay_off():
    relay_pin.value(0)

turn_relay_on()
time.sleep(2) 
turn_relay_off() 