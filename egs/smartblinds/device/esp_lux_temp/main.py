from umqtt.simple import MQTTClient
from machine import Pin
import ubinascii
import machine
import ujson as json
import gc
import time
import ntptime
import onewire, ds18x20
import tsl2591

config = open("config.json", "r")
cfg = json.load(config)
config.close()

ntptime.settime()

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
client = MQTTClient(CLIENT_ID, cfg["mqtt"]["broker"], cfg["mqtt"]["port"], cfg["mqtt"]["user"], cfg["mqtt"]["passwd"])
client.connect()

ds = ds18x20.DS18X20(onewire.OneWire(Pin(4)))
roms = ds.scan()

sta_if = network.WLAN(network.STA_IF)

def measure_temp():
    ds.convert_temp()
    return ds.read_temp(roms[0])

tsl = tsl2591.Tsl2591()

def measure_send():
    lux = tsl.measure()
    temp = measure_temp()

    lux_msg = {"value": lux, "quantity": "illuminance"}
    temp_msg = {"value": temp, "quantity": "temperature"}
    print(f'Illuminance: {lux} lux\nTemperature: {temp}°C')

    msgs = [lux_msg, temp_msg]
    topics = [cfg["mqtt"]["lux_topic"], cfg["mqtt"]["temp_topic"]]
    for msg, topic in zip(msgs, topics):
        client.publish(topic, json.dumps(msg))
    print("Successfully published messages.\n")

try:
    while 1:
        measure_send()
        time.sleep(cfg["period"])
finally:
    client.disconnect()