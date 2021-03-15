from modules.voicehome_module import VoicehomeModule
import requests
import json

# "move_id": "weather_01.get_forecast_today",
# "method_name": "get_forecast_today",
# "description": "Getting forecast for today by web scratch technic.",
# "calls": [["dnešní předpověď"], ["předpověď"], ["jak dneska bude"]]

class Weather(VoicehomeModule):

    def __init__(self, engine, dir_path, active):
        VoicehomeModule.__init__(self, engine, dir_path, active)
        self.token_owm = '937cc176a1bf7fc717c10cb41b83d0b3'
        self.location_lon = 13.3776
        self.location_lat = 49.7475

    def on_mqtt_message(self, msg):
        print('Module ' + self.id + ": start sending mqtt")
        pass

    def on_websocket_message(self, msg):
        print('Module ' + self.id + ": start sending websocket")
        if msg['message'] == "webWeatherOWM":
            msg['reply'] = self.webWeatherOWM()
            self.websocket_send(msg)
        print("Sensors: websocket sended")
        pass

    def get_forecast_today(self):
        pass

    def webWeatherOWM(self):
        print('Module ' + self.id + ": start sending webWeather from OWM")
        # Design API uri (see the OpenWeatherMap DOC)
        api_uri = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&exclude=hourly,minutely&appid={}'.format(self.location_lat, self.location_lon, self.token_owm)

        response = requests.get(api_uri)
        print('OWM Response status:', response.status_code)  # 2xx is OK

        # Get json
        data_owm = response.json()
        # print('Weather data:', data_owm)

        buffer = {
            "current_time": data_owm["current"]['dt'],
            "current_temperature": data_owm["current"]['temp'],
            "today_icon": data_owm["daily"][0]['weather'][0]['icon'],
            "tomorrow_icon": data_owm["daily"][1]['weather'][0]['icon'],
            "today_temperature_day": data_owm["daily"][0]['temp']['day'],
            "today_temperature_night": data_owm["daily"][0]['temp']['night'],
            "tomorrow_temperature_day": data_owm["daily"][1]['temp']['day'],
            "tomorrow_temperature_night": data_owm["daily"][1]['temp']['night']
        }
        if 'rain' in data_owm["daily"][1].keys():
            buffer["tomorrow_rain"]= data_owm["daily"][1]['rain']
        else:
            buffer["tomorrow_rain"]= '0'

        if 'rain' in data_owm["daily"][0].keys():
            buffer["today_rain"]= data_owm["daily"][0]['rain']
        else:
            buffer["today_rain"]= '0'

        print('Module ' + self.id + ": ending sending webWeather from OWM")
        return buffer