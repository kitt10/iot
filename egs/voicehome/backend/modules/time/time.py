from modules.voicehome_module import VoicehomeModule

class Time(VoicehomeModule):

    def __init__(self, engine, dir_path):
        VoicehomeModule.__init__(self, engine, dir_path)

    def get_time(self):
        print("Sending current time")

    def get_day(self):
        print("Sending current day")
        
    def set_timer(self):
        time = 3
        print("Setting timer on " + time + "minute")

    def stop_timer(self):
        print("Timer is stopped.")