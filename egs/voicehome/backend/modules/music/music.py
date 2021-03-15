from modules.voicehome_module import VoicehomeModule

class Music(VoicehomeModule):

    def __init__(self, engine, dir_path, active):
        VoicehomeModule.__init__(self, engine, dir_path, active)

    def on_mqtt_message(self, msg):
        print('Module ' + self.id + ": start sending mqtt")
        pass

    def on_websocket_message(self, msg):
        print('Module '+self.id+": start sending websocket")
        pass

    def play_music(self):
        payload = {
            'type': 'music',
            'set': 'play'
        }
        self.mqtt_publish(topic='voicehome/music', payload=payload)
        print('Module ' + self.id + ': command to play music.')

    def stop_music(self,message=True):
        payload = {
            'type': 'music',
            'set': 'stop'
        }
        self.mqtt_publish(topic='voicehome/music', payload=payload)
        if message:
            print('Module ' + self.id + ': command to stop music.')
        
    def play_radio(self):
        payload = {
            'type': 'radio',
            'set': 'play'
        }
        self.mqtt_publish(topic='voicehome/music', payload=payload)
        print('Module ' + self.id + ': command to play radio.')

    def stop_radio(self,message=True):
        payload = {
            'type': 'music',
            'set': 'stop'
        }
        self.mqtt_publish(topic='voicehome/music', payload=payload)
        if message:
            print('Module ' + self.id + ': command to stop music.')

    def shutup(self):
        self.stop_music(message=False)
        self.stop_radio(message=False)
        print('Module ' + self.id + ': command to stop music and radio.')
