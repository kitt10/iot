from os import listdir
from os.path import isdir, join as join_path
from importlib import import_module


class VoicehomeModulesPort:

    def __init__(self, engine):
        self.engine = engine
        self.cfg = engine.cfg

        self.modules = []
        self.modules_off = []
        self.modules_off_names = []
        self.load_modules()

    def load_modules(self):
        for dir_item in listdir('modules'):
            dir_path = join_path('modules', dir_item)
            if isdir(dir_path) and dir_item not in ['__pycache__']:
                module = import_module('modules.'+dir_item+'.'+dir_item)
                cls = getattr(module, dir_item.capitalize())
                if dir_item not in self.modules_off_names:
                    self.modules_off.append(cls(engine=self.engine, dir_path=dir_path))
                else:
                    self.modules.append(cls(engine=self.engine, dir_path=dir_path))

    def reload_modules(self):
        self.modules = []
        self.engine.logic.moves = {}
        self.engine.webserver.packet['modules'] = []
        self.engine.webserver.packet['modules_off'] = []
        self.engine.webserver.subscriptions = []
        self.engine.mqtt.subscriptions = []
        self.load_modules()

    def turn_module_on(self, module_id):
        print('Turning on', module_id)
        try:
            self.modules_off_names.remove(module_id)
        except ValueError:
            return

        self.reload_modules()

    def turn_module_off(self, module_id):
        print('Turning off', module_id)
        if module_id not in self.modules_off_names:
            self.modules_off_names.append(module_id)

        self.reload_modules()
