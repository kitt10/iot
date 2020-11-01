from json import load as load_json
from os.path import join as join_path


class VoicehomeModule:

    def __init__(self, engine, dir_path):
        self.engine = engine
        self.cfg = engine.cfg
        self.dir_path = dir_path

        self.id = None
        self.version = None
        self.actions = []

        self.load_metadata()

        print('Module', self.id, 'loaded.')

    def load_metadata(self):
        with open(join_path(self.dir_path, 'metadata.json'), 'r') as f:
            metadata = load_json(f)

        self.id = metadata['module_id']
        self.version = metadata['version']
        self.actions = metadata['actions']
