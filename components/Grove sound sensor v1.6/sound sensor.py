import machine
import time

sound_pin = machine.Pin(4, machine.Pin.IN)

while True:

    sound_value = sound_pin.value()

    print("Sound value:", sound_value)

    time.sleep(0.1)