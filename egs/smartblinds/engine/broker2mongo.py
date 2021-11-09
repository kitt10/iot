from yaml import full_load as yaml_full_load
import paho.mqtt.client as mqtt_client
from pymongo import MongoClient
from datetime import datetime
from json import loads as json_loads


class MQTTSubscriber:

    def __init__(self, cfg, mongo):
        self.cfg = cfg
        self.mongo = mongo
        self.client = mqtt_client.Client(client_id='smartblinds_broker2mongo')
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log
        self.client.username_pw_set(self.cfg['broker']['uname'], password=self.cfg['broker']['passwd'])
        self.run_subscriber()

    def on_connect(self, client, userdata, mid, qos):
        if self.cfg['verbose']:
            log(self.cfg, 'Connected to broker with result code qos: '+str(qos))

        self.client.subscribe(self.cfg['broker']['topic'])

    def on_message(self, client, userdata, msg):
        if (msg.payload == 'Q'):
            self.client.disconnect()

        self.mongo.save(item=json_loads(msg.payload), topic=str(msg.topic))

    def on_log(self, client, userdata, level, buf):
        if self.cfg['broker']['verbose']:
            print('MQTT LOG:', buf)

    def run_subscriber(self):
        self.client.connect(self.cfg['broker']['host'], self.cfg['broker']['port'], 60)
        self.client.loop_forever()


class Mongo:

    def __init__(self, cfg):
        self.cfg = cfg
        self.mongoClient = MongoClient(self.cfg['mongo']['host'], self.cfg['mongo']['port'])
        self.database = self.mongoClient[self.cfg['mongo']['database']]
        self.collection = self.database[self.cfg['mongo']['collection']]

    def save(self, item, topic):
        timestamp = datetime.now().isoformat()
        item.update({'timestamp': timestamp, 'topic': topic, 'location': topic.split('/')[2]})
        self.collection.insert_one(item)
        self.log(str(timestamp)+'\tSaved.\t'+str(item['quantity'])+' at '+str(item['location'])+': '+str(item['value']))

    def log(self, buf):
        if self.cfg['mongo']['verbose']:
            print('MONGO LOG:', buf)


def load_config(cfg_file):
    with open(cfg_file, 'r') as fr:
        cfg = yaml_full_load(fr)

    log(cfg, 'Config file '+str(cfg_file)+' loaded.')
    return cfg

def log(cfg, buf):
    if cfg['verbose']:
        print('MAIN LOG:', buf)


if __name__ == '__main__':

    # Load config
    cfg = load_config(cfg_file='cfg_engine.yml')

    # Init MongoDB
    mongo = Mongo(cfg)

    # Run MQTT subscriber
    MQTTSubscriber(cfg, mongo)
