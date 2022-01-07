import paho.mqtt.client as mqtt_client
import time
from pyowm.owm import OWM
import json

class Collector:
    def __init__(self, config_file="cfg_collector.json"):
        cfg_file = open(config_file, "r")
        self.cfg = json.load(cfg_file)
        cfg_file.close()

        owm = OWM(self.cfg["owm"]["key"])
        self.mgr = owm.weather_manager()

        self.features = {f: None for f in self.cfg["mqtt"]["features"]}
        self.targets = {t: None for t in self.cfg["mqtt"]["targets"]}

        self.client = mqtt_client.Client(client_id = 'OWM')
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.cfg["mqtt"]["user"], password = self.cfg["mqtt"]["passwd"])
        self.client.connect(self.cfg["mqtt"]["broker"], self.cfg["mqtt"]["port"])

        last_time = time.time()-60*self.cfg["period"]-1
        while True:
            if last_time+60*self.cfg["period"]<time.time():
                last_time = time.time()
                self.periodical = True
                self.request_values()
            self.client.loop()
                

    def on_connect(self, client, userdata, mid, qos):
        self.client.subscribe([(topic, 0) for topic in self.cfg["mqtt"]["event_topics"]])
        self.client.subscribe([(topic, 0) for topic in self.cfg["mqtt"]["features"].values()])
        self.client.subscribe([(topic, 0) for topic in self.cfg["mqtt"]["targets"].values()])

    def get_time(self):
        (year, month, mday, hour, minute, sec, wd, yd, isdst) = time.localtime()
        seconds = hour*3600 + minute*60 + sec
        return (yd, wd, seconds)

    def reset_values(self):
        self.features = {f: None for f in self.features}
        self.targets = {t: None for t in self.targets}

    def on_message(self, client, userdata, message):
        print(message.payload)
        if message.topic in self.cfg["mqtt"]["event_topics"] and not self.pending_request:
            self.periodical = False
            self.request_values()
        elif message.topic == self.cfg["mqtt"]["testing_topic"]:
            try:
                msg = json.loads(message.payload.decode('utf-8'))
                quantity_id = msg["id"]
                print(quantity_id)
                if quantity_id=="testing":
                    self.cfg["testing"] = msg["value"]
                    print("Set testing mode to ", self.cfg["testing"])
            except:
                print("E: unable to set testing value.", message.topic, message.payload)
        else:
            try:
                msg = json.loads(message.payload.decode('utf-8'))
                quantity_id = msg["id"]
                print(quantity_id)
                if quantity_id in self.cfg["mqtt"]["features"]:
                    self.features[quantity_id] = msg["value"]
                else:
                    self.targets[quantity_id] = msg["value"]
            except:
                print("E: json.loads")
            if not None in self.features.values() and not None in self.targets.values():
                self.send_sample()
        print(self.features)
        print(str(self.targets) + "\n")

    def request_values(self):
        self.pending_request = True
        msg={
            "timestamp": time.time(),
            "testing": self.cfg["testing"],
            "periodical": self.periodical,
            "command": "request_values"
        }
        self.client.publish(self.cfg["mqtt"]["request_topic"], json.dumps(msg))
        
    def get_owm(self):
        one_call = self.mgr.one_call(lat = self.cfg["owm"]["lat"], lon = self.cfg["owm"]["lon"])
        values = dict(
            owm_temp_1h = one_call.forecast_hourly[1].temperature('celsius')["temp"],
            owm_temp_2h = one_call.forecast_hourly[2].temperature('celsius')["temp"],
            owm_temp_3h = one_call.forecast_hourly[3].temperature('celsius')["temp"],
            owm_temp_max = one_call.forecast_daily[0].temperature('celsius')["max"],
            owm_wind_speed = one_call.forecast_hourly[0].wind().get('speed', 0),
            owm_wind_heading = one_call.forecast_hourly[0].wind().get('deg', 0),
            owm_code = one_call.forecast_hourly[0].weather_code
        )
        
        return values

    def send_sample(self):
        (yd, wd, ds) = self.get_time()
        for i in range(3):
            try:
                owm_vals = self.get_owm()
                break
            except:
                time.sleep(1)
                pass
            
        sample = {
            "timestamp": time.time(),          
            "testing": self.cfg["testing"],            
            "periodical": self.periodical,         
            "features": {
                "year_day": yd,         
                "week_day": wd,         
                "day_secs": ds
            },
            "targets": self.targets
        }
        sample["features"].update(owm_vals)
        sample["features"].update(self.features)

        message = json.dumps(sample)

        self.client.publish(self.cfg["mqtt"]["sample_topic"], message)
        self.pending_request = False
        self.reset_values()

        print(message)

if __name__ == "__main__":
    Collector()