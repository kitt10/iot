from modules.voicehome_module import VoicehomeModule
import json

class Lights(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)
        self.lightsList = {}
        self.reloadLightsList()

    def ESP_turn_light_on_onboard(self, ESP_ID):
        payload = {
            'ID':ESP_ID,
            'type': 'ESP_onboard',
            'set': 1
        }
        self.mqtt_publish(topic='voicehome/lights/command', payload=payload)

    def ESP_turn_light_off_onboard(self, ESP_ID):
        payload = {
            'ID':ESP_ID,
            'type': 'ESP_onboard',
            'set': 0
        }
        self.mqtt_publish(topic='voicehome/lights/command', payload=payload)

    def ESP_turn_light_on(self, light_ID):
        payload = {
            'ID':light_ID,
            'type': 'light',
            'set': 1
        }
        self.mqtt_publish(topic='voicehome/lights/command', payload=payload)

    def ESP_turn_light_off(self, light_ID):
        payload = {
            'ID':light_ID,
            'type': 'light',
            'set': 0
        }
        self.mqtt_publish(topic='voicehome/lights/command', payload=payload)

    def ESP_turn_light_on_1(self):
        print('Module ' + self.id + ": turning light 1 on")
        self.ESP_turn_light_on(1)

    def ESP_turn_light_off_1(self):
        print('Module ' + self.id + ": turning light 1 off")
        self.ESP_turn_light_off(1)

    def ESP_turn_light_on_onboard_1(self):
        self.ESP_turn_light_on_onboard(1)

    def ESP_turn_light_on_onboard_2(self):
        print('Module ' + self.id + ": turning ESP id = 1 onboard light on")
        self.ESP_turn_light_on_onboard(2)

    def ESP_turn_light_on_onboard_3(self):
        self.ESP_turn_light_on_onboard(3)

    def ESP_turn_light_off_onboard_1(self):
        print('Module ' + self.id + ": turning ESP id = 1 onboard light off")
        self.ESP_turn_light_on_onboard(1)

    def ESP_turn_light_off_onboard_2(self):
        self.ESP_turn_light_on_onboard(2)

    def ESP_turn_light_off_onboard_3(self):
        self.ESP_turn_light_on_onboard(3)

    def turn_ESP_onboard_led_on(self):
        self.ESP_turn_light_on_onboard('all')

    def turn_ESP_onboard_led_off(self):
        self.ESP_turn_light_off_onboard('all')

    def on_mqtt_message(self, msg):
        print('Module ' + self.id + ": start sending mqtt")
        pass

    def on_websocket_message(self, msg):
        print('Module ' + self.id + ": start sending websocket")
        pass

    def reloadLightsList(self):
        print('Module ' + self.id + ": reloadLightsList")
        # print(os.getcwd())
        with open('modules/lights/lightsList.json') as json_file:
            self.lightsList = json.load(json_file)
