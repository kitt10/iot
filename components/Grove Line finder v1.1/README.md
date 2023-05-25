## Line finder v1.1

<table border="0" width="100%"><tr><td colspan=2 width="60%">seeed studio Grove </td>
<td rowspan=9 width="40%" align="right"><img src="../../.img/line.jpg" width="200px" /></td></tr>
<tr><td>Voltage range</td><td><b>5V</b></td></tr>
<tr><td>Input type</td><td><b>Digital</b></td></tr>
<tr><td>Compatible</td><td><b>Arduino, Raspberry Pi, ESP8266</b></td></tr>
<tr><td>Response time</td><td><b>1s</b></td></tr>
<tr><td>Price</td><td><b>< 92 Kč</b></td></tr></table>

* [Datasheet](./datasheet.pdf)

### Circuit
<p align="center"><img src="../../.img/line.png" width="45%" /></p>

### MicroPython

```python
import machine
import time

line_pin = machine.Pin(4, machine.Pin.IN)

while True:

    line_value = line_pin.value()

    if line_value == 1:
        print("line not found")
    else:
        print("line found")

    time.sleep(0.1)
```

### Notes
> Also found in Grove Creator Kit-
>
>https://wiki.seeedstudio.com/Grove-Creator-Kit-1/

### References
> https://wiki.seeedstudio.com/Grove-Line_Finder/
>
> https://seeeddoc.github.io/Grove-Line_Finder/

### Zpracováno
- Václav Sontag
- Lucas Löffler