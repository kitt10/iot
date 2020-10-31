from ..vh_module import VoicehomeModule


class System(VoicehomeModule):

    def __init__(self, engine):
        VoicehomeModule.__init__(self, engine)

    def test_mqtt(self):
        print('Testing MQTT on', self.cfg.mqtt.port)
        pass

    def test_database(self):
        print('Testing Database on', self.cfg.mongo.port)
        pass
