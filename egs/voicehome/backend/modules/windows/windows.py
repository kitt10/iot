from modules.voicehome_module import VoicehomeModule

class Windows(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)

    def pull_blinds(self):
        print("Pulling blinds")

    def expand_blinds(self):
        print("Expand blinds")
        
    def check_windows(self):
        print("Checking windows")