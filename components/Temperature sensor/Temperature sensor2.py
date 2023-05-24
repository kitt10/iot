import dht
import machine
import time

dht_pin = machine.Pin(4)
dht_sensor = dht.DHT11(dht_pin)

while True:
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()

        print("Temperature: {:.2f} Degrees".format(temperature))
        time.sleep(3)

    except OSError as e:
        time.sleep(3)