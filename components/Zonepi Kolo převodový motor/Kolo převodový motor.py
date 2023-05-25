import machine
import time

motor_pin = machine.Pin(4, machine.Pin.OUT)

def turn_on_motor():
    motor_pin.on()

def turn_off_motor():
    motor_pin.off()

while True:
    turn_on_motor()
    time.sleep(1)
    turn_off_motor()
    time.sleep(1)