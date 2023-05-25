import machine
import time

SENZOR_PIN = machine.Pin(4, machine.Pin.IN)

def read_sensor_value():
    return SENZOR_PIN.value()

while True:
    sensor_value = read_sensor_value()
    print("Hodnota senzoru: {}".format(sensor_value))
time_sleep(1)