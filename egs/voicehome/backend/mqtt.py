from paho.mqtt.client import Client as MQTTClient
from threading import Thread, ThreadError
from json import loads as json_loads


class VoicehomeMQTTClient(MQTTClient):

    def __init__(self, engine):
        MQTTClient.__init__(self)
        self.engine = engine
        self.cfg = engine.cfg
        self.username_pw_set(self.cfg.mqtt.uname, password=self.cfg.mqtt.passwd)
        self.connect(self.cfg.mqtt.host, self.cfg.mqtt.port)

        try:
            t = Thread(target=self.loop_forever)
            t.setDaemon(True)
            t.start()
        except ThreadError:
            print('ERR: Thread MQTT')

    def on_connect(self, client, userdata, flags, rc):
        print('MQTT Client: Connected with result code qos:', rc)
        self.subscribe(self.cfg.mqtt.topic)

    def on_message(self, client, userdata, msg):

        try:
            payload = json_loads(msg.payload.decode('utf-8'))
        except AttributeError:
            payload = json_loads(msg.payload)

        print('New MQTT Message:', payload)

    def on_disconnect(self, client, userdata, rc):
        print('MQTT Client: Disconnected with result code qos:', rc)