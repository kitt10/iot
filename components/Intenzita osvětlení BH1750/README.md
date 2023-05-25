## Intenzita osvětlení

<table border="0" width="100%"><tr><td colspan=2 width="60%"></td>
<td rowspan=9 width="40%" align="right"><img src="../../.img/intenz.jpg" width="200px" /></td></tr>
<tr><td>Voltage range</td><td><b>3.3V - 5V</b></td></tr>
<tr><td>Compatible</td><td><b>Arduino, Raspberry Pi, ESP8266</b></td></tr>
<tr><td>Response time</td><td><b>2ms</b></td></tr>
<tr><td>Measuring range</td><td><b>0 - 65535lux</b></td></tr></table>
<tr><td>Price</td><td><b>< 67 Kč</b></td></tr></table>

* [Datasheet not found]()

### Circuit
<p align="center"><img src="../../.img/intenz.png" width="45%" /></p>

### MicroPython

```python

from machine import Pin
import time
sda_pin = Pin(4, Pin.OUT)
scl_pin = Pin(5, Pin.OUT)
def start_transmission():
    sda_pin.value(1)
    scl_pin.value(1)
    sda_pin.value(0)
    scl_pin.value(0)
def stop_transmission():
    scl_pin.value(0)
    sda_pin.value(0)
    scl_pin.value(1)
    sda_pin.value(1)
def read_light_intensity():
    start_transmission()
    scl_pin.value(1)
    time.sleep_ms(180)
    scl_pin.value(0)
    stop_transmission()
    return sda_pin.value()
while True:
    light_level = read_light_intensity()
    if light_level == 1:
        print("Light detected")
    else:
        print("Light not detected")
    time.sleep(1)
```

### References
> https://www.laskakit.cz/snimac-intenzity-osvetleni-bh1750/
>
> https://rpishop.cz/svetlo/2435-modul-intenzity-svetla-gy-302-bh1750.html

### Zpracováno
- Václav Sontag
- Lucas Löffler