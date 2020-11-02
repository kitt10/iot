from modules.voicehome_module import VoicehomeModule


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
        pass
