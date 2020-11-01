from json import load as load_json
from os.path import join as join_path


class VoicehomeModule:

    def __init__(self, engine, dir_path):
        self.engine = engine
        self.cfg = engine.cfg
        self.dir_path = dir_path

        self.id = None
        self.version = None
        self.module_moves = []

        self.load_metadata()
        self.register_actions()

        print('Module', self.id, 'loaded ('+str(len(self.module_moves))+' moves).' )

    def load_metadata(self):
        with open(join_path(self.dir_path, 'metadata.json'), 'r') as f:
            metadata = load_json(f)

        self.id = metadata['module_id']
        self.version = metadata['version']
        self.module_moves = metadata['moves']

        self.engine.webserver.packet['modules'].append(metadata)

    def register_actions(self):
        for move in self.module_moves:
            method = getattr(self, move['method_name'])
            self.engine.logic.moves[move['move_id']] = (method, move['calls'])

    def reply(self, msg):
        self.engine.control.new_reply(msg)
