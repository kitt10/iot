import machine
import time

light_pin = machine.Pin(4, machine.Pin.IN)

while True:

    light_value = light_pin.value()

    print("Light value:", light_value)

    time.sleep(0.1)
