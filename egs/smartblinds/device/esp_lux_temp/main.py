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

def get_time():
    try:
        ntptime.settime()
    except:
        pass
    (year, month, mday, hour, minute, sec, wd, yd) = time.localtime(3600*cfg["tz"] + time.mktime(time.localtime()))
    seconds = hour*3600 + minute*60 + sec
    return (yd, wd, seconds)

def measure_temp():
    ds.convert_temp()
    return ds.read_temp(roms[0])

def measure_send():
    lux = tsl.measure()
    temp = measure_temp()

    time_keys = ["year_day", "week_day", "day_seconds"]
    time_tuple = get_time()
    time_dict = {time_keys[i]: time_tuple[i] for i in range(len(time_keys))}

    lux_msg = {"time": time_dict, "value": lux, "quantity": "illuminance", "id": cfg["ids"]["lux"]}
    temp_msg = {"time": time_dict, "value": temp, "quantity": "temperature", "id": cfg["ids"]["temp"]}
    print('Illuminance: {} lux\nTemperature: {}°C'.format(lux, temp))

    msgs = [lux_msg, temp_msg]
    topics = [cfg["mqtt"]["lux_topic"], cfg["mqtt"]["temp_topic"]]
    for msg, topic in zip(msgs, topics):
        client.publish(topic, json.dumps(msg))
    print("Successfully published messages.\n")

def callback(topic, message):
    measure_send()


config = open("config.json", "r")
cfg = json.load(config)
config.close()

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
client = MQTTClient(CLIENT_ID, cfg["mqtt"]["broker"], cfg["mqtt"]["port"], cfg["mqtt"]["user"], cfg["mqtt"]["passwd"])
client.set_callback(callback)

client.connect()
for event_topic in cfg["mqtt"]["event_topics"]: client.subscribe(event_topic)
ow = onewire.OneWire(Pin(cfg["ds_pin"]))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

sta_if = network.WLAN(network.STA_IF)

tsl = tsl2591.Tsl2591()

last_time = time.time()-cfg["period"]
while 1:
    if sta_if.isconnected():
        if(time.time()-last_time>=cfg["period"]):
            measure_send()
            last_time = time.time()
        client.check_msg()
    else:
        connect()
        client.connect()