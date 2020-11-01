from os import listdir
from os.path import isdir, join as join_path
from importlib import import_module


class VoicehomeModulesPort:

    def __init__(self, engine):
        self.engine = engine
        self.cfg = engine.cfg

        self.modules = []
        self.load_modules()

    def load_modules(self):
        for dir_item in listdir('modules'):
            dir_path = join_path('modules', dir_item)
            if isdir(dir_path) and dir_item not in ('__pycache__',):
                module = import_module('modules.'+dir_item+'.'+dir_item)
                cls = getattr(module, dir_item.capitalize())
                self.modules.append(cls(engine=self.engine, dir_path=dir_path))

    def reload_modules(self):
        self.modules = []
        self.engine.logic.moves = {}
        self.engine.webserver.packet['modules'] = []
        self.load_modules()
