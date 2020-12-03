from modules.voicehome_module import VoicehomeModule

class Music(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)

    def play_music(self):
        print("I am playing music")

    def stop_music(self):
        print("I am stopping music")
        
    def play_radio(self):
        print("I am playing radio")

    def stop_radio(self):
        print("I am stopping radio")

    def shutup(self):
        print("I am quiet")