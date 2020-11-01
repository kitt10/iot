from modules.voicehome_module import VoicehomeModule


class System(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)

    def test_mqtt(self):
        print('Testing MQTT on', self.cfg.mqtt.port)
        self.reply('MQTT tested.')

    def test_database(self):
        print('Testing Database on', self.cfg.mongo.port)
        self.reply('Database tested.')
