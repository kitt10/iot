import paho.mqtt.client as mqtt_client
import time
from pyowm.owm import OWM
import json

def on_connect(client, userdata, mid, qos):
    client.subscribe([(topic, 0) for topic in cfg["mqtt"]["event_topics"]])

def get_time():
    (year, month, mday, hour, minute, sec, wd, yd, isdst) = time.localtime()
    seconds = hour*3600 + minute*60 + sec
    return (yd, wd, seconds)

def on_message(client, userdata, message):
    one_call = mgr.one_call(lat = cfg["owm"]["lat"], lon = cfg["owm"]["lon"])
    temperature = one_call.forecast_daily[1].temperature('celsius')["day"]

    time_keys = ["year_day", "week_day", "day_seconds"]
    time_tuple = get_time()
    time_dict = {time_keys[i]: time_tuple[i] for i in range(len(time_keys))}

    msg = {"quantity": "forecast_temperature", "time": time_dict, "value": temperature}
    message = json.dumps(msg)
    client.publish(cfg["mqtt"]["topic"], message)
    print(message)



cfg_file = open("cfg_owm.json", "r")
cfg = json.load(cfg_file)
cfg_file.close()
owm = OWM(cfg["owm"]["key"])
mgr = owm.weather_manager()

client = mqtt_client.Client(client_id = 'OWM')
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(cfg["mqtt"]["user"], password = cfg["mqtt"]["passwd"])
client.connect(cfg["mqtt"]["broker"], cfg["mqtt"]["port"])
client.loop_forever()