## Temperature & humi sensor

<table border="0" width="100%"><tr><td colspan=2 width="60%">seeed studio Grove </td>
<td rowspan=9 width="40%" align="right"><img src="../../.img/humi.jpg" width="200px" /></td></tr>
<tr><td>Voltage range</td><td><b>3.3V - 5V</b></td></tr>
<tr><td>Input type</td><td><b>Digital</b></td></tr>
<tr><td>Compatible</td><td><b>Arduino, Raspberry Pi, ESP8266</b></td></tr>
<tr><td>Temperature Measuring Range</td><td><b>-0°C to +70°C</b></td></tr>
<tr><td>Humidity Measuring Range</td><td><b>20% to 90% RH</b></td></tr>
<tr><td>Response time</td><td><b>2s</b></td></tr>
<tr><td>Price</td><td><b>< 248 Kč</b></td></tr></table>

* [Datasheet not found]()

### Circuit
<p align="center"><img src="../../.img/humi.png" width="45%" /></p>

### MicroPython

```python
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
```

### Notes
> Also found in Grove Creator Kit-
>
>https://wiki.seeedstudio.com/Grove-Creator-Kit-1/

### References
> https://wiki.seeedstudio.com/Grove-TemperatureAndHumidity_Sensor/
>
> https://seeeddoc.github.io/Grove-Temperature_and_Humidity_Sensor/

### Zpracováno
- Václav Sontag
- Lucas Löffler