from modules.voicehome_module import VoicehomeModule


class Sensors(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)

    def on_mqtt_message(self):
        pass

    def on_websocket_message(self):
        pass
