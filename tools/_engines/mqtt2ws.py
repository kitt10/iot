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
from json import dumps as dumps_json


def parse_arguments():  
    parser = ArgumentParser(description='mqtt2ws')
    parser.add_argument('-c', '--cfg_path', type=str, default='webserver.cfg',
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

        payload = json_loads(msg.payload.decode('utf-8'))
        print('\n MQTT message\n\tTopic: {} \n\tPayload: {}'.format(msg.topic, payload))
        
        try:
            t = Thread(target=self.process_and_send_ws, args=[payload])
            t.setDaemon(True)
            t.start()
        except ThreadError:
            print('ERR: Thread MQTT')
        
    def process_and_send_ws(self, payload):
        global pointers
        for handler in pointers['ws_handlers']:
            iol.spawn_callback(handler.write_message, dumps_json(payload))
        
    def on_disconnect(self, client, userdata, rc):
        print('MQTT Client: Disconnected with result code qos:', rc)

class MainHandler(TornadoRequestHandler):

    def get(self):
        self.render('index.html')

class WSHandler(WebSocketHandler):

    def initialize(self):
        global pointers
        pointers['ws_handlers'].append(self)
        print('A new WS handler initialized. Connected clients:', len(pointers['ws_handlers']))

    def open(self):
        print('WS server: Websocket opened.')
        self.write_message(u'WS server: Server ready.')

    def on_message(self, message):
        print('WS server: message received.')
        try:
            print(json_loads(message.decode('utf-8')))
        except ValueError:
            print(message)

    def send_message(self, params):
        self.write_message(dumps_json(params))

    def on_close(self):
        global pointers
        pointers['ws_handlers'].remove(self)
        print('WS server: A websocket client closed. Connected clients:', len(pointers['ws_handlers']))


if __name__ == '__main__':
    
    # Print Python version, load project configuration
    cfg = load_config()

    # Load trained classifiers
    pointers = {'ws_handlers': list()}

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
        (r'/(.*)', StaticFileHandler, {
            'path': join_path(dirname(__file__), './')})
    ], debug=debug_web, autoreload=debug_web)
    
    app.listen(cfg.tornado.port)
    iol = IOLoop.current()
    iol.start()
