import machine
import time

sensor_pin = machine.Pin(4, machine.Pin.IN)

while True:

    sensor_value = sensor_pin()

    sensor_percentage = sensor_value

    print("Hodnota: {}%".format(sensor_percentage))

    time.sleep(0.1)