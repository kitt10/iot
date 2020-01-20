from sys import version as py_version
from argparse import ArgumentParser
from config import Config
from os.path import dirname, join as join_path
from paho.mqtt.client import Client as ClientMQTT
from threading import Thread, ThreadError
from tornado.web import StaticFileHandler, RequestHandler as TornadoRequestHandler, Application as TornadoApplication
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from websocket import WebSocketApp
from json import load as load_json, dump as dump_json, loads as json_loads, dumps as dumps_json
from datetime import datetime, date
import numpy as np

from model import load_clfs, new_model, prepare_json_clf
from data import Sample


def parse_arguments():  
    parser = ArgumentParser(description='Smarthome sensory system - engine')
    parser.add_argument('-c', '--cfg_path', type=str, default='config.cfg',
                        help='Path to the config file.')

    return parser.parse_args()

def load_config():
    args = parse_arguments()
    print('\n\n')
    print(py_version)
    print('Config file:', args.cfg_path)
    print('------------------------------------------------')
    with open(args.cfg_path, 'r') as f:
        return Config(f)

def load_models():
    with open('models.json', 'r') as f:
        return load_json(f)

class MQTT(ClientMQTT):

    def __init__(self, cfg):
        ClientMQTT.__init__(self)
        self.cfg = cfg
        self.username_pw_set(cfg.mqtt.uname, password=cfg.mqtt.passwd)

    def on_connect(self, client, userdata, flags, rc):
        print('MQTT Client: Connected with result code qos:', rc)
        self.subscribe(self.cfg.mqtt.topic)

    def on_message(self, client, userdata, msg):
        global pointers

        try:
            payload = json_loads(msg.payload.decode('utf-8'))
        except AttributeError:
            payload = json_loads(msg.payload)

        print('\n MQTT message\n\tTopic: {} \n\tPayload: {}'.format(msg.topic, payload))

        clf = pointers['clfs'][payload['owner']][payload['location']][payload['quantity']]

        # Classify and send in a new thread
        try:
            t = Thread(target=self.predict_and_send_ws, args=[clf, payload])
            t.setDaemon(True)
            t.start()
        except ThreadError:
            print('ERR: Thread MQTT')

    def predict_and_send_ws(self, clf, payload):
        global pointers
        sample = Sample(data=payload, today=date.today())
        dim = pointers['models'][payload['owner']][payload['location']][payload['quantity']]['dim']

        if sample.status == 'ok' and pointers['ws_handlers']:
            if dim == 2:
                payload['classification'] = int(clf.predict([[sample.secOfDay, sample.value]])[0])
            elif dim == 1:
                payload['classification'] = int(clf.predict([[sample.secOfDay]])[0])
            
            payload['type'] = 'newSample'
            for handler in pointers['ws_handlers']:
                iol.spawn_callback(handler.write_message, dumps_json(payload))
        else:
            print('W: sample not OK', payload)

    def on_disconnect(self, client, userdata, rc):
        print('MQTT Client: Disconnected with result code qos:', rc)

class MainHandler(TornadoRequestHandler):

    def get(self):
        self.render('../frontend/index.html')

class JsonHandler(TornadoRequestHandler):
    def get(self):
        self.write(dumps_json(pointers['json_clfs']))

class WSHandler(WebSocketHandler):

    def initialize(self):
        global pointers
        pointers['ws_handlers'].append(self)
        print('A new WS handler initialized. Connected clients:', len(pointers['ws_handlers']))

    def open(self):
        print('WS server: Websocket opened.')
        self.write_message(u'WS server: Server ready.')

    def on_message(self, message):
        global pointers
        print('WS server: <- '+str(message))
        try:
            params = json_loads(message)
            if params['type'] == 'retrainModel':
                new_model(topic=params['topic'], 
                          date_from=params['date_from'],
                          date_to=params['date_to'],
                          sensors=params['sensors'],
                          cfg=cfg,
                          owner=params['owners'])
                
                return
                # register new model - TODO
                _, location, quantity = params['topic'].split('/')
                for sensor in params['sensors']:
                    pointers['json_clfs']['pn'][location][quantity][sensor] = prepare_json_clf(pointers)

        except ValueError:
            pass

    def on_close(self):
        global pointers
        pointers['ws_handlers'].remove(self)
        print('WS server: A websocket client closed. Connected clients:', len(pointers['ws_handlers']))


if __name__ == '__main__':
    
    # Print Python version, load project configuration
    cfg = load_config()

    # Load trained classifiers
    clfs, json_clfs = load_clfs(cfg)
    pointers = {'ws_handlers': list(), 'clfs': clfs, 'models': load_models(), 'json_clfs': json_clfs}

    mqtt_client = MQTT(cfg)
    mqtt_client.connect(cfg.mqtt.host)
    try:
        t = Thread(target=mqtt_client.loop_forever)
        t.setDaemon(True)
        t.start()
    except ThreadError:
        print('ERR: Thread MQTT')

    debug_web = True
    app = TornadoApplication([
        (r'/', MainHandler),
        (r'/websocket', WSHandler),
        (r"/json_clfs/", JsonHandler),
        (r'/(.*)', StaticFileHandler, {
            'path': join_path(dirname(__file__), '../')})
    ], debug=debug_web, autoreload=debug_web)
    
    app.listen(cfg.tornado.port)
    iol = IOLoop.current()
    iol.start()
