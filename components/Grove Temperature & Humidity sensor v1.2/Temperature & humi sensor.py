import dht
import machine
import time

dht_pin = machine.Pin(4)
dht_sensor = dht.DHT11(dht_pin)

while True:
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        print("Temperature: {:.2f} Degrees".format(temperature))
        print("Humidity: {:.2f}%".format(humidity))
        time.sleep(3)

    except OSError as e:
        print("Error reading sensor data:", e)
        time.sleep(3)
