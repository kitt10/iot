from machine import Pin
import time

trigger_pin = Pin(5, Pin.OUT) # trigger D1
echo_pin = Pin(4, Pin.IN) #echo D2

def measure_distance():

    trigger_pin.on()
    time.sleep_us(10)
    trigger_pin.off()

    while echo_pin.value() == 0:
        pulse_start = time.ticks_us()

    while echo_pin.value() == 1:
        pulse_end = time.ticks_us()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 0.0343 / 2 # Převod času na vzdálenost

    return distance

while True:
    distance = measure_distance()
    print("distance:", distance, "cm")
    time.sleep(1)