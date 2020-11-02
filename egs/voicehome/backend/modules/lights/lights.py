from modules.voicehome_module import VoicehomeModule


class Lights(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)

    def turn_led_on(self):
        payload = {
            'led_id': 'onboard',
            'set': 1
        }
        self.mqtt_publish(topic='voicehome/lights/led', payload=payload)

    def turn_led_off(self):
        payload = {
            'led_id': 'onboard',
            'set': 0
        }
        self.mqtt_publish(topic='voicehome/lights/led', payload=payload)

    def on_mqtt_message(self, msg):
        pass

    def on_websocket_message(self, msg):
        pass
