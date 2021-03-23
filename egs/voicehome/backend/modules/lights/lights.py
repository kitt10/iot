from modules.voicehome_module import VoicehomeModule
import json


class Lights(VoicehomeModule):

    def __init__(self, engine, dir_path, active):
        VoicehomeModule.__init__(self, engine, dir_path, active)
        self.lightsList = {}
        self.reloadLightsList()
        self.requestStateEachLight()


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
        self.mqtt_publish(topic='voicehome/lights/command', payload=payload)
        # self.requestState(ESP_ID, 'ESP_onboard')

    def ESP_turn_off_light_onboard(self, ESP_ID):
        payload = {
            'ID':ESP_ID,
            'type': 'ESP_onboard',
            'set': 1
        }
        self.mqtt_publish(topic='voicehome/lights/command', payload=payload)
        # self.requestState(ESP_ID, 'ESP_onboard')

    def ESP_turn_on_light(self, light_ID):
        payload = {
            'ID':light_ID,
            'type': 'light',
            'set': 1
        }
        self.mqtt_publish(topic='voicehome/lights/command', payload=payload)
        # self.requestState(light_ID, 'light')



    def ESP_turn_off_light(self, light_ID):
        payload = {
            'ID':light_ID,
            'type': 'light',
            'set': 0
        }
        self.mqtt_publish(topic='voicehome/lights/command', payload=payload)
        # self.requestState(light_ID, 'light')

    def ESP_turn_on_light_1(self):
        print('Module ' + self.id + ": turning light 1 on")
        self.ESP_turn_on_light(1)
        self.reply(message='Světlo v obývacím pokoji rozsvíceno')

    def ESP_turn_off_light_1(self):
        print('Module ' + self.id + ": turning light 1 off")
        self.ESP_turn_off_light(1)
        self.reply(message='Světlo v obývacím pokoji zhasnuto')

    def ESP_turn_on_light_onboard_1(self):
        self.ESP_turn_on_light_onboard(1)
        self.reply(message='Vývojová deska číslo jedna rozsvícena')

    def ESP_turn_on_light_onboard_2(self):
        print('Module ' + self.id + ": turning ESP id = 1 onboard light on")
        self.ESP_turn_on_light_onboard(2)
        self.reply(message='Vývojová deska číslo dva rozsvícena')

    def ESP_turn_on_light_onboard_3(self):
        self.ESP_turn_on_light_onboard(3)
        self.reply(message='Vývojová deska číslo tři rozsvícena')

    def ESP_turn_off_light_onboard_1(self):
        print('Module ' + self.id + ": turning ESP id = 1 onboard light off")
        self.ESP_turn_off_light_onboard(1)
        self.reply(message='Vývojová deska číslo jedna zhasnuta')

    def ESP_turn_off_light_onboard_2(self):
        self.ESP_turn_off_light_onboard(2)
        self.reply(message='Vývojová deska číslo dva zhasnuta')

    def ESP_turn_off_light_onboard_3(self):
        self.ESP_turn_off_light_onboard(3)
        self.reply(message='Vývojová deska číslo tři zhasnuta')

    def turn_on_ESP_onboard_led(self):
        for esp in self.lightsList['ESP_onboard']:
            self.ESP_turn_on_light_onboard(esp['ID'])
        self.reply(message='Všechny vývojové desky rozsvíceny')

    def turn_off_ESP_onboard_led(self):
        for esp in self.lightsList['ESP_onboard']:
            self.ESP_turn_off_light_onboard(esp['ID'])
        self.reply(message='Všechny vývojové desky zhasnuty')

    def on_mqtt_message(self, msg):
        print('Module ' + self.id + ": start sending mqtt")
        payload = msg.payload.decode('utf8').replace("'", '"')
        payload = json.loads(payload)
        if msg.topic == "voicehome/lights/state/receive":
            if payload['type'] in self.lightsList.keys():
                for light in self.lightsList[payload['type']]:
                    if payload['ID'] == light['ID']:
                        if payload['type'] == 'ESP_onboard':
                            if payload['state'] == 1:
                                light['state']=0
                            else:
                                light['state']=1
                        else:
                            light['state']=payload['state']


            msg1={}
            msg1['passport'] = "lights/state"
            msg1['message'] = "lightsList"
            msg1['reply'] = self.lightsList
            try:
                self.websocket_send(msg1)
            except:
                print('Unenable to send websocket at module Lights on_mqtt_message()')
                pass
        pass

    def on_websocket_message(self, msg):
        print('Module ' + self.id + ": start sending websocket")
        print(msg)
        if msg['passport'] == "lights/state":
            if msg['message'] == "lightsList":
                # self.requestStateEachLight()
                msg1 = {}
                msg1['passport'] = "lights/state"
                msg1['message'] = "lightsList"
                msg1['reply'] = self.lightsList
                self.websocket_send(msg1)
            if msg['message'] == "lightCommand":
                if msg['second_param']['type'] == 'ESP_onboard':
                    if msg['second_param']['set'] == 1:
                        self.ESP_turn_on_light_onboard(msg['second_param']['ID'])
                    if msg['second_param']['set'] == 0:
                        self.ESP_turn_off_light_onboard(msg['second_param']['ID'])
                if msg['second_param']['type'] == 'light':
                    if msg['second_param']['set'] == 1:
                        self.ESP_turn_on_light(msg['second_param']['ID'])
                    if msg['second_param']['set'] == 0:
                        self.ESP_turn_off_light(msg['second_param']['ID'])
        pass

    def reloadLightsList(self):
        print('Module ' + self.id + ": reloadLightsList")
        # print(os.getcwd())
        with open('modules/lights/lightsList.json') as json_file:
            self.lightsList = json.load(json_file)

    def which_lights_on(self):
        lights_on=''
        for type in self.lightsList:
            print('type')
            print(type)
            for light in self.lightsList[type]:
                print('light')
                print(light)
                if 'state' in light:
                    if light['state']==1:
                        if lights_on=='':
                            lights_on = lights_on + light['description']
                        else:
                            lights_on = lights_on + ', ' + light['description']

        if lights_on == '':
            self.reply(message='Aktuálně nejsou rozsvícena žádná světla')
        else:
            self.reply(message='Aktuálně jsou rozsvícena tyto světla ' + lights_on)