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
    values = dict(
        temp_1h = one_call.forecast_hourly[1].temperature('celsius')["temp"],
        temp_2h = one_call.forecast_hourly[2].temperature('celsius')["temp"],
        temp_3h = one_call.forecast_hourly[3].temperature('celsius')["temp"],
        max_temp = one_call.forecast_daily[0].temperature('celsius')["max"],
        wind_speed = one_call.forecast_hourly[0].wind().get('speed', 0),
        wind_heading = one_call.forecast_hourly[0].wind().get('deg', 0),
        code = one_call.forecast_hourly[0].weather_code
    )

    time_keys = ["year_day", "week_day", "day_seconds"]
    time_tuple = get_time()
    time_dict = {time_keys[i]: time_tuple[i] for i in range(len(time_keys))}

    for q in values:
        msg = {"quantity": cfg["QUANTITIES"][q], "id": q, "time": time_dict, "value": values[q]}
        message = json.dumps(msg)
        client.publish(cfg["mqtt"]["topics"][q], message)
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
on_message(client, "", "")
client.loop_forever()