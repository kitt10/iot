from paho.mqtt.client import Client as MQTTClient
from json import loads as json_loads


class VoicehomeMQTTClient(MQTTClient):

    def __init__(self, engine):
        MQTTClient.__init__(self)
        self.engine = engine
        self.cfg = engine.cfg
        self.username_pw_set(self.cfg.mqtt.uname, password=self.cfg.mqtt.passwd)
        self.connect(self.cfg.mqtt.host, self.cfg.mqtt.port)

    def run_loop(self):
        self.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        self.subscribe(self.cfg.mqtt.topic)
        print('MQTT Client: Connected. Subscribed to', self.cfg.mqtt.topic)

    def on_message(self, client, userdata, msg):
        print('MQTT Client: New Message:', msg.payload)

    def on_disconnect(self, client, userdata, rc):
        print('MQTT Client: Disconnected.')
