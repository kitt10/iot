from modules.voicehome_module import VoicehomeModule
import json

class Sensors(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)

    def get_current_temperature(self):
        payload = {
            'command': 'measure_now',
            'quantity': 'temperature'
        }
        self.mqtt_publish(topic='voicehome/sensors/commands', payload=payload)
        print('Module '+self.id+': command to measure temperature sent.')

    def on_mqtt_message(self, msg):
        if msg['key'] == 'current_temperature':
            self.reply(message='Aktuální teplota je: '+str(msg['value']))

    def on_websocket_message(self, msg):
        print("Sensors: start sending websocket")
        print(msg)
        if msg['message'] == "whole_temperature_data":
            msg['reply'] = self.whole_temperature_data(msg)
            self.websocket_send(msg)
        print("Sensors: websocket sended")
        pass

    def whole_temperature_data(self, msg):
        print("Sensors: sending whole temperature data")
        query = {'key': 'voicehome/sensors/test'}
        res = self.search_mongo(self.id, query)
        buffer = []
        for res_i in res:
            result_i = res_i["payload"].decode("utf8")
            buffer.append(json.loads(result_i))
        return buffer
