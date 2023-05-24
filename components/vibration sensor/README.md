## Vibration sensor

<table border="0" width="100%"><tr><td colspan=2 width="60%">seeed studio Grove </td>
<td rowspan=9 width="40%" align="right"><img src="../../.img/vibrsen.jpg" width="200px" /></td></tr>
<tr><td>Voltage range</td><td><b>3.5V - 5V</b></td></tr>
<tr><td>Input type</td><td><b>Digital</b></td></tr>
<tr><td>Compatible</td><td><b>Arduino, Raspberry Pi, ESP8266</b></td></tr>
<tr><td>Dynamic range</td><td><b>0.1Hz~180Hz</b></td></tr>
<tr><td>Response time</td><td><b>1s</b></td></tr>
<tr><td>Price</td><td><b>< 75 Kč</b></td></tr></table>

* [Datasheet](./datasheet.pdf)

### Circuit
<p align="center"><img src="../../.img/vibrsen.png" width="45%" /></p>

### MicroPython

```python
import machine
import time

sensor_pin = machine.Pin(4, machine.Pin.IN)

while True:
    if sensor_pin.value() == 1:
        print("Vibrace nedetekovana")
       
    else:
        print("Vibrace detekovana!")
    time.sleep(0.1)
```

### Notes
> Also found in Grove Creator Kit-
>
>https://wiki.seeedstudio.com/Grove-Creator-Kit-1/

### References
> https://wiki.seeedstudio.com/Grove-Piezo_Vibration_Sensor/
>
> https://www.tme.eu/en/details/seeed-101020586/other-sensors/seeed-studio/vibration-sensor-sw-420/

### Zpracováno
- Václav Sontag
- Lucas Löffler