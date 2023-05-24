## Light sensor v1.2

<table border="0" width="100%"><tr><td colspan=2 width="60%">seeed studio Grove </td>
<td rowspan=9 width="40%" align="right"><img src="../../.img/light.jpg" width="200px" /></td></tr>
<tr><td>Voltage range</td><td><b>3V - 5V</b></td></tr>
<tr><td>Input type</td><td><b>Digital</b></td></tr>
<tr><td>Compatible</td><td><b>Arduino, Raspberry Pi, ESP8266</b></td></tr>
<tr><td>Peak wavelength</td><td><b>540 nm</b></td></tr>
<tr><td>Response time</td><td><b>20-30ms</b></td></tr>
<tr><td>Price</td><td><b>< 71 Kč</b></td></tr></table>

* [Datasheet](./datasheet.pdf)

### Circuit
<p align="center"><img src="../../.img/light.png" width="45%" /></p>

### MicroPython

```python
import machine
import time

light_pin = machine.Pin(4, machine.Pin.IN)

while True:

    light_value = light_pin.value()

    print("Light value:", light_value)

    time.sleep(0.1)
```

### Notes
> Also found in Grove Creator Kit-
>
> https://wiki.seeedstudio.com/Grove-Creator-Kit-1/

### References
> https://wiki.seeedstudio.com/Grove-Light_Sensor/
>
> https://seeeddoc.github.io/Grove-Light_Sensor_v1.2/

### Zpracováno
- Václav Sontag
- Lucas Löffler