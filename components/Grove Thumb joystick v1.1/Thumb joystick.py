import machine
import time

x_pin = machine.Pin(4, machine.Pin.IN) # X pin D2
y_pin = machine.Pin(2, machine.Pin.IN) # Y pin D4

def read_joystick():
    x_state = x_pin.value()
    y_state = y_pin.value()
    return x_state, y_state

while True:
    x, y = read_joystick()
    print("X-axis state:", x)
    time.sleep(1)
    print("Y-axis state:", y)
    time.sleep(1)
    print("------------------")
    time.sleep(1)