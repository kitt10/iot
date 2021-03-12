from modules.voicehome_module import VoicehomeModule
import json


class Lights(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)
        self.lightsList = {}
        self.reloadLightsList()
        # self.requestStateEachLight()


    def requestState(self,ID,type):
        payload = {
            'ID': ID,
            'type': type
        }
        self.mqtt_publish(topic='voicehome/lights/state/command', payload=payload)
        
    def requestStateEachLight(self):
        for esp in self.lightsList['ESP_onboard']:
            self.requestState(esp['ID'],'ESP_onboard')

        for light in self.lightsList['light']:
            self.requestState(light['ID'],'light')


    def ESP_turn_on_light_onboard(self, ESP_ID):
        payload = {
            'ID':ESP_ID,
            'type': 'ESP_onboard',
            'set': 0
        }
        for esp in self.lightsList['ESP_onboard']:
            if esp['ID'] == ESP_ID:
                esp['state'] = 1
        self.mqtt_publish(topic='voicehome/lights/command', payload=payload)

    def ESP_turn_off_light_onboard(self, ESP_ID):
        payload = {
            'ID':ESP_ID,
            'type': 'ESP_onboard',
            'set': 1
        }
        for esp in self.lightsList['ESP_onboard']:
            if esp['ID'] == ESP_ID:
                esp['state'] = 0
        self.mqtt_publish(topic='voicehome/lights/command', payload=payload)

    def ESP_turn_on_light(self, light_ID):
        payload = {
            'ID':light_ID,
            'type': 'light',
            'set': 1
        }
        for light in self.lightsList['light']:
            if light['ID'] == light_ID:
                light['state'] = 1
        self.mqtt_publish(topic='voicehome/lights/command', payload=payload)



    def ESP_turn_off_light(self, light_ID):
        payload = {
            'ID':light_ID,
            'type': 'light',
            'set': 0
        }
        for light in self.lightsList['light']:
            if light['ID'] == light_ID:
                light['state'] = 0
        self.mqtt_publish(topic='voicehome/lights/command', payload=payload)

    def ESP_turn_on_light_1(self):
        print('Module ' + self.id + ": turning light 1 on")
        self.ESP_turn_on_light(1)

    def ESP_turn_off_light_1(self):
        print('Module ' + self.id + ": turning light 1 off")
        self.ESP_turn_off_light(1)

    def ESP_turn_on_light_onboard_1(self):
        self.ESP_turn_on_light_onboard(1)

    def ESP_turn_on_light_onboard_2(self):
        print('Module ' + self.id + ": turning ESP id = 1 onboard light on")
        self.ESP_turn_on_light_onboard(2)

    def ESP_turn_on_light_onboard_3(self):
        self.ESP_turn_on_light_onboard(3)

    def ESP_turn_off_light_onboard_1(self):
        print('Module ' + self.id + ": turning ESP id = 1 onboard light off")
        self.ESP_turn_off_light_onboard(1)

    def ESP_turn_off_light_onboard_2(self):
        self.ESP_turn_off_light_onboard(2)

    def ESP_turn_off_light_onboard_3(self):
        self.ESP_turn_off_light_onboard(3)

    def turn_on_ESP_onboard_led(self):
        for esp in self.lightsList['ESP_onboard']:
            self.ESP_turn_on_light_onboard(esp['ID'])

    def turn_off_ESP_onboard_led(self):
        for esp in self.lightsList['ESP_onboard']:
            self.ESP_turn_off_light_onboard(esp['ID'])

    def on_mqtt_message(self, msg):
        print('Module ' + self.id + ": start sending mqtt")
        payload = msg.payload.decode('utf8').replace("'", '"')
        payload = json.loads(payload)
        if msg.topic == "voicehome/lights/state/receive":
            if payload['type'] in self.lightsList.keys():
                for light in self.lightsList[payload['type']]:
                    if payload['ID'] == light['ID']:
                        light['state']=payload['state']

            msg={}
            msg['passport'] = "lights/state"
            msg['message'] = "lightsList"
            msg['reply'] = self.lightsList
            try:
                self.websocket_send(msg)
            except:
                print('Unenable to send websocket at module Lights on_mqtt_message()')
                pass
        pass

    def on_websocket_message(self, msg):
        print('Module ' + self.id + ": start sending websocket")
        print(msg)
        if msg['passport'] == "lights/state":
            if msg['message'] == "lightsList":
                msg['reply'] = self.lightsList
                self.websocket_send(msg)
        pass

    def reloadLightsList(self):
        print('Module ' + self.id + ": reloadLightsList")
        # print(os.getcwd())
        with open('modules/lights/lightsList.json') as json_file:
            self.lightsList = json.load(json_file)
