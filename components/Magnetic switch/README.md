## Magnetic switch

<table border="0" width="100%"><tr><td colspan=2 width="60%">seeed studio Grove </td>
<td rowspan=9 width="40%" align="right"><img src="../../.img/Magnetic switch.jpg" width="200px" /></td></tr>
<tr><td>Voltage range</td><td><b>3.3V - 5.25V</b></td></tr>
<tr><td>Input type</td><td><b>Digital</b></td></tr>
<tr><td>Compatible</td><td><b>Arduino, Raspberry Pi, ESP8266</b></td></tr>
<tr><td>Operating temperature</td><td><b>-40°C to +125°C</b></td></tr>
<tr><td>Response time</td><td><b>1s</b></td></tr>
<tr><td>Price</td><td><b>< 72 Kč</b></td></tr></table>

* [Datasheet](./datasheet.pdf)

### Circuit
<p align="center"><img src="../../.img/Magnetic switch.png" width="45%" /></p>

### MicroPython

```python
import machine
import time

switch_pin = machine.Pin(4, machine.Pin.IN)

while True:
    if switch_pin.value() == 0:
        print("off")
   
    else:
        print("on")
    time.sleep(0.1)
```

### Notes
> Also found in Grove Creator Kit-
>
>https://wiki.seeedstudio.com/Grove-Creator-Kit-1/

### References
> https://wiki.seeedstudio.com/Grove-Magnetic_Switch/
>
> https://cz.rs-online.com/web/p/vyvojove-nastroje-pro-snimace/1793718

### Zpracováno
- Václav Sontag
- Lucas Löffler