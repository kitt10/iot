from modules.voicehome_module import VoicehomeModule


class Sensors(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)

    def on_mqtt_message(self, msg):
        print('Module', self.id, 'doing something with MQTT msg', msg)

    def on_websocket_message(self, msg):
        pass
