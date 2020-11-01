from modules.voicehome_module import VoicehomeModule


class System(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)

    def reload_modules(self):
        print('Module system: Reloading modules...')
        self.engine.port.reload_modules()
        self.reply('Modules reloaded.')

    def test_database(self):
        print('Testing Database on', self.cfg.mongo.port)
        self.reply('Database tested.')
