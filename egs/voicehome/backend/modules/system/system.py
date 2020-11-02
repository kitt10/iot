from modules.voicehome_module import VoicehomeModule
from datetime import datetime


class System(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)

    def reload_modules(self):
        print('Module system: Reloading modules...')
        self.engine.port.reload_modules()
        self.reply('Modules reloaded.')

    def test_database(self):
        print('Testing Database on', self.cfg.mongo.host, ':', self.cfg.mongo.port)
        try:
            testing_payload = {
                'key': 'test',
                'datetime': datetime.now()
            }
            self.save_to_mongo(module_id=self.id, payload=testing_payload)
            res = self.search_mongo(module_id=self.id, query={'key': 'test'})
            self.reply('Module ' + self.id + ': Database tested. OK. Found items: '+str(len(res)))
        except Exception as e:
            self.reply('Module '+self.id+': Error testing database: '+str(e))
