## LED Socket Kit

<table border="0" width="100%"><tr><td colspan=2 width="60%">seeed studio Grove </td>
<td rowspan=9 width="40%" align="right"><img src="../../.img/LED Socket Kit v1.5.jpg" width="200px" /></td></tr>
<tr><td>Voltage range</td><td><b>3.3V - 5V</b></td></tr>
<tr><td>Input type</td><td><b>Digital</b></td></tr>
<tr><td>Compatible</td><td><b>Arduino, Raspberry Pi, ESP8266</b></td></tr>
<tr><td>Operating temperature</td><td><b>-25°C to +70°C</b></td></tr>
<tr><td>Response time</td><td><b>1s</b></td></tr>
<tr><td>Price</td><td><b>< 46 Kč</b></td></tr></table>

* [Datasheet](./datasheet.pdf)

### Circuit
<p align="center"><img src="../../.img/LED Socket Kit v1.5.png" width="45%" /></p>

### MicroPython

```python
import machine
import time

pin = machine.Pin(4, machine.Pin.OUT)

def turn_on():
    pin.on()

def turn_off():
    pin.off()

while True:
    turn_on()
    time.sleep(5)
    turn_off()
    time.sleep(1)
```

### Notes
> Multiple variations exist (green, red, blue, white)
>
> Also found in Grove Creator Kit-
>
>https://wiki.seeedstudio.com/Grove-Creator-Kit-1/

### References
> https://wiki.seeedstudio.com/Grove-LED_Socket_Kit/
>
> https://simple-circuit.com/arduino-led-blink-seeed-studio-grove-led-socket-kit/
### Zpracováno
- Václav Sontag
- Lucas Löffler