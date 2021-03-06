from modules.voicehome_module import VoicehomeModule

class Windows(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)

    def pull_blinds(self):
        payload = {
            'type': 'blinds',
            'set': 'pull'
        }
        self.mqtt_publish(topic='voicehome/windows', payload=payload)
        print('Module ' + self.id + ': command to pull blinds.')

    def expand_blinds(self):
        payload = {
            'type': 'blinds',
            'set': 'expand'
        }
        self.mqtt_publish(topic='voicehome/windows', payload=payload)
        print('Module ' + self.id + ': command to expand blinds.')
        
    def check_windows(self):
        payload = {
            'type': 'windows',
            'set': 'check'
        }
        self.mqtt_publish(topic='voicehome/windows', payload=payload)
        print('Module ' + self.id + ': command to check windows.')