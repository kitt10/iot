from paho.mqtt.client import Client as MQTTClient
from threading import Thread, ThreadError


class VoicehomeMQTTClient(MQTTClient):

    def __init__(self, engine):
        MQTTClient.__init__(self)
        self.engine = engine
        self.cfg = engine.cfg

        self.subscriptions = []

        self.username_pw_set(self.cfg.mqtt.uname, password=self.cfg.mqtt.passwd)
        self.connect(self.cfg.mqtt.host, self.cfg.mqtt.port)

    def run_loop(self):
        self.loop_forever()

    def publish(self, payload, topic, qos=0, retain=False):
        self.publish(payload, topic, qos, retain)
        print('MQTT: Published to', topic)

    def on_connect(self, client, userdata, flags, rc):
        self.subscribe(self.cfg.mqtt.topic)
        print('MQTT: Connected. Subscribed to', self.cfg.mqtt.topic)

    def on_message(self, client, userdata, msg):
        print('MQTT: New Message:', msg.payload)
        for (module_id, method, subscribing_list) in self.subscriptions:
            if msg.topic in subscribing_list:
                print('MQTT: Module', module_id, 'interested.')
                try:
                    t = Thread(target=method, args=(msg,))
                    t.setDaemon(True)
                    t.start()
                except ThreadError:
                    print('ERR: Thread MQTT Message-Module', module_id)

    def on_disconnect(self, client, userdata, rc):
        print('MQTT: Disconnected.')
