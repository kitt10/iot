from json import load as load_json
from os.path import join as join_path


class VoicehomeModule:

    def __init__(self, engine, dir_path):
        self.engine = engine
        self.cfg = engine.cfg
        self.dir_path = dir_path

        self.id = None
        self.version = None
        self.mqtt_topics = []
        self.websocket_passports = []
        self.module_moves = []

        self.load_metadata()
        self.register_moves()
        self.register_subscriptions()

        print('Module', self.id, 'loaded ('+str(len(self.module_moves))+' moves).' )

    def load_metadata(self):
        with open(join_path(self.dir_path, 'metadata.json'), 'r') as f:
            metadata = load_json(f)

        self.id = metadata['module_id']
        self.module_moves = metadata['moves']
        self.mqtt_topics = metadata['mqtt_topics']
        self.websocket_passports = metadata['websocket_passports']

        if self.id in self.engine.port.modules_off_names:
            self.engine.webserver.packet['modules_off'].append(metadata)
        else:
            self.engine.webserver.packet['modules'].append(metadata)

    def register_moves(self):
        for move in self.module_moves:
            method = getattr(self, move['method_name'])
            self.engine.logic.moves[move['move_id']] = (method, move['calls'])

    def register_subscriptions(self):
        if self.mqtt_topics:
            self.engine.mqtt.subscriptions.append((self.id, self.on_mqtt_message, self.mqtt_topics))

        if self.websocket_passports:
            self.engine.webserver.subscriptions.append((self.id, self.on_websocket_message, self.websocket_passports))

    def reply(self, message):
        self.engine.control.new_reply(message)

    def mqtt_publish(self, topic, payload):
        self.engine.mqtt.new_publish(topic, payload)

    def websocket_send(self, msg):
        self.engine.webserver.app.ws_message(msg)

    def search_mongo(self, module_id, query):
        return self.engine.db.read(module_id, query)

    def save_to_mongo(self, module_id, payload):
        self.engine.db.write(module_id, payload)

    def on_mqtt_message(self, msg):
        pass

    def on_websocket_message(self, msg):
        pass
