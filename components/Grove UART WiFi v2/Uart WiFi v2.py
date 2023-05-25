import machine
import time
import network

uart = machine.UART(0, 115200) 
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("Xiaomi 11T", "12345678")
time.sleep(5)
if wifi.isconnected():
    print("Připojeno k Wi-Fi síti")
else:
    print("Chyba při připojování k Wi-Fi síti")
while True:
    uart.write(b"Hello, World!\n")
    time.sleep(1)
 # bílý na pin TX
 # žlutý na pin RX
 # VCC na pin 3.3v
 # GND na pin GND