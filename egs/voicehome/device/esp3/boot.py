import esp
import gc
import network
import machine
import time
import config

import uasyncio as asyncio
from machine import UART
uart = UART(0, 115200)

async def sender():
    swriter = asyncio.StreamWriter(uart, {})
    while True:
        await swriter.awrite('Hello uart\n')
        await asyncio.sleep(2)

async def receiver():
    sreader = asyncio.StreamReader(uart)
    while True:
        res = await sreader.readline()
        print('Recieved', res)

async def wait_and_kill(loop):
    while True:
        print('you have 3 sec')
        await asyncio.sleep(3)
        loop.stop()

loop = asyncio.get_event_loop()
loop.create_task(sender())
loop.create_task(receiver())
loop.create_task(wait_and_kill(loop))
loop.run_forever()


esp.osdebug(None)
# esp.sleep_type(0)
gc.collect()
# time.sleep(6)

def connect():
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config.WIFI['SSID'],config.WIFI['PASSWD'])
        while not sta_if.isconnected():
            time.sleep_ms(500)
    print('network config:', sta_if.ifconfig())

try:
    connect()
except:
    print('can not connect wifi')
    machine.reset()