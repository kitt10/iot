import machine
import time

sensor_pin = machine.Pin(4, machine.Pin.IN)

while True:
    if sensor_pin.value() == 1:
        print("Vibrace nedetekovana")
       
    else:
        print("Vibrace detekovana!")
    time.sleep(0.1)