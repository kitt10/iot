import machine
import time

water_pin = machine.Pin(4, machine.Pin.IN)

while True:

    water_value = water_pin.value()

    if water_value:
        print("Soil is dry")
    else:
        print("Soil is wet")

    time.sleep(0.1)