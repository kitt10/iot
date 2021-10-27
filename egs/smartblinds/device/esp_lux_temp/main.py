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
from connect import connect
import network

config = open("config.json", "r")
cfg = json.load(config)
config.close()

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
client = MQTTClient(CLIENT_ID, cfg["mqtt"]["broker"], cfg["mqtt"]["port"], cfg["mqtt"]["user"], cfg["mqtt"]["passwd"])
client.connect()
ow = onewire.OneWire(Pin(cfg["ds_pin"]))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

sta_if = network.WLAN(network.STA_IF)

def measure_temp():
    ds.convert_temp()
    return ds.read_temp(roms[0])

tsl = tsl2591.Tsl2591()

def get_time():
    try:
        ntptime.settime()
    except:
        pass
    (year, month, mday, hour, minute, sec, wd, yd) = time.localtime(3600*cfg["tz"] + time.mktime(time.localtime()))
    seconds = hour*3600 + minute*60 + sec
    return (yd, wd, seconds)

def measure_send():
    lux = tsl.measure()
    temp = measure_temp()

    time_keys = ["year_day", "week_day", "day_seconds"]
    time_tuple = get_time()
    time_dict = {time_keys[i]: time_tuple[i] for i in range(len(time_keys))}

    lux_msg = {"time": time_dict, "value": lux, "quantity": "illuminance"}
    temp_msg = {"time": time_dict, "value": temp, "quantity": "temperature"}
    print('Illuminance: {} lux\nTemperature: {}°C'.format(lux, temp))

    msgs = [lux_msg, temp_msg]
    topics = [cfg["mqtt"]["lux_topic"], cfg["mqtt"]["temp_topic"]]
    for msg, topic in zip(msgs, topics):
        client.publish(topic, json.dumps(msg))
    print("Successfully published messages.\n")


while 1:
    if sta_if.isconnected():
        measure_send()
        time.sleep(cfg["period"])
    else:
        connect()
        client.connect()