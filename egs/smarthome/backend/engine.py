from sys import version as py_version
from argparse import ArgumentParser
from config import Config
from os.path import dirname, join as join_path
from paho.mqtt.client import Client as ClientMQTT
from threading import Thread, ThreadError, Timer
from tornado.web import StaticFileHandler, RequestHandler as TornadoRequestHandler, Application as TornadoApplication
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from websocket import WebSocketApp
from json import load as load_json, dump as dump_json, loads as json_loads, dumps as dumps_json
from datetime import datetime, date
from time import ctime
import time
import numpy as np
import os

from model import load_clfs, load_clf, new_model, prepare_json_clf
from data import Sample

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


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

def watcher():
    print('Timer', ctime())

class MQTT(ClientMQTT):

    def __init__(self, cfg):
        ClientMQTT.__init__(self)
        self.cfg = cfg
        self.username_pw_set(cfg.mqtt.uname, password=cfg.mqtt.passwd)
        self.create_json_file()
        self.ds18b20_01 = 0
        self.ds18b20_02 = 0
        self.dht11_01 = 0
        self.tsl2591_01 = 0
        self.bme280_01 = 0
        self.keys = []
        
    def create_json_file(self):
        webpage_data = os.path.isfile('webpage_data.json') 
        if not webpage_data:
            with open('webpage_data.json', 'w') as json_file: 
                json_data = dict()
                dump_json(json_data, json_file, indent=2)
                
    def update_data(self,payload):
        data['am312_01'] = [1,'2020-02-21 00:00:00','ok']
        if payload['sensor_id'] == 'bme280_01' and payload['quantity'] == 'temperature':
            pass
        else: 
            data[payload['sensor_id']] = [payload['value'],payload['timestamp'],payload['status']] 
            with open('webpage_data.json', 'w+') as f:
                dump_json(data, f, indent=2)            

    def on_connect(self, client, userdata, flags, rc):
        print('MQTT Client: Connected with result code qos:', rc)
        self.subscribe(self.cfg.mqtt.topic)

    def on_message(self, client, userdata, msg):
        global pointers

        try:
            payload = json_loads(msg.payload.decode('utf-8'))
        except AttributeError:
            payload = json_loads(msg.payload)

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

        if sample.status == 'ok': #and pointers['ws_handlers']:
            if dim == 2:
                payload['classification'] = int(clf.predict([[sample.secOfDay, sample.value]])[0])
            elif dim == 1:
                payload['classification'] = int(clf.predict([[sample.secOfDay]])[0])
            
            if payload['classification'] < 0:
                print("Sample status OK and Clasif -1")
                payload['status'] = 'value_error'

        elif payload['status'] is not 'ok':
            print("Sample status NOT ok")
            payload['status'] = 'error'  
            
        payload['type'] = 'newSample'
        for handler in pointers['ws_handlers']:
            iol.spawn_callback(handler.write_message, dumps_json(payload))

        # Check the next one
        sensor_key = payload['owner']+':'+payload['location']+':'+payload['quantity']+':'+payload['sensor_id']
        pointers['last_sample_timestamp'][sensor_key] = payload['timestamp']
        Timer(80, self.sensor_check, [payload]).start()    
            
            #if payload['classification'] == 1:
            #    payload['page_info'] = 'ok'
            #elif payload['classification'] == -1:
            #    payload['page_info'] = 'value_error'

        #elif sample.status == 'sensor_error' or 'ds18b20_inside_error' or 'ds18b20_outside_error' or 'dht11_error':
            #print('status ERR')
            #payload['value'] = 0
            #payload['page_info'] = 'error'

        #payload['type'] = 'newSample'
        #for handler in pointers['ws_handlers']:
            #iol.spawn_callback(handler.write_message, dumps_json(payload))
            #iol.spawn_callback(handler.write_message, dumps_json({'location': 'heheh', 'owner': 'pn', 'status': 'ok'}))

        try:
            t = Thread(target=self.update_data(payload), args=[clf, payload])
            t.setDaemon(True)
            t.start()
        except ThreadError:
            print('ERR: Thread UPDATE DATA')        

    def sensor_check(self, payload):
        sensor_key = payload['owner']+':'+payload['location']+':'+payload['quantity']+':'+payload['sensor_id']
        dt_last = datetime.strptime(pointers['last_sample_timestamp'][sensor_key], '%Y-%m-%d %H:%M:%S')
        dt_now = datetime.now()
        seconds_diff = (dt_now-dt_last).total_seconds()
        if seconds_diff > 60:
            print('ERR: sensor_dead:', sensor_key)
            payload['status'] = 'error'
            payload['value'] = 0
            payload['classification'] = 0
            payload['type'] = 'newSample'
            for handler in pointers['ws_handlers']:
                iol.spawn_callback(handler.write_message, dumps_json(payload))

    def on_disconnect(self, client, userdata, rc):
        print('MQTT Client: Disconnected with result code qos:', rc)

class MainHandler(TornadoRequestHandler):

    def get(self):
        self.render('../frontend/overview.html')

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
            if params['type'] == 'newModel':
                new_model(topic=params['topic'], 
                          date_from=params['date_from'],
                          date_to=params['date_to'],
                          sensors=params['sensors'],
                          cfg=cfg,
                          owner=params['owner'])
                
                print('New model trained.', params)

                pointers['models'] = load_models()

                _, location, quantity = params['topic'].split('/')
                pointers['clfs'][params['owner']][location][quantity], pointers['json_clfs'][params['owner']][location][quantity] = load_clf(pointers['models'], params['owner'], location, quantity, params['sensors'], cfg)

                print('CLF json updated.')
                for handler in pointers['ws_handlers']:
                    iol.spawn_callback(handler.write_message, dumps_json({'type': 'newModelReady'}))
            
            elif params['type'] == 'selectModel':
                model_name = params['model_name']
                owner, location, quantity, sensors_, _ = model_name.split(':')
                sensors = sensors_.split('&')
                
                pointers['models'][owner][location][quantity]['active'] = model_name
                pointers['clfs'][owner][location][quantity], pointers['json_clfs'][owner][location][quantity] = load_clf(pointers['models'], owner, location, quantity, sensors, cfg)

                # Save the models metadata
                with open('models.json', 'w') as f:
                    dump_json(pointers['models'], f)
                
                print('New model selected:', model_name)
                for handler in pointers['ws_handlers']:
                    iol.spawn_callback(handler.write_message, dumps_json({'type': 'newModelReady'}))

        except ValueError:
            pass

    def on_close(self):
        global pointers
        pointers['ws_handlers'].remove(self)
        print('WS server: A websocket client closed. Connected clients:', len(pointers['ws_handlers']))


if __name__ == '__main__':
    data = dict()
    
    # Print Python version, load project configuration
    cfg = load_config()

    # Load trained classifiers
    clfs, json_clfs = load_clfs(cfg)
    pointers = {'ws_handlers': list(), 
                'clfs': clfs, 
                'models': load_models(), 
                'json_clfs': json_clfs,
                'last_sample_timestamp': dict()}

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
