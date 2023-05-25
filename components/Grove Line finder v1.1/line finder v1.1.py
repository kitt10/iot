import machine
import time

line_pin = machine.Pin(4, machine.Pin.IN)

while True:

    line_value = line_pin.value()

    if line_value == 1:
        print("line not found")
    else:
        print("line found")

    time.sleep(0.1)