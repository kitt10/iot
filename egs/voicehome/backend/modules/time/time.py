from modules.voicehome_module import VoicehomeModule
import datetime
import threading 

class Time(VoicehomeModule):

    def __init__(self, engine, dir_path, active):
        VoicehomeModule.__init__(self, engine, dir_path, active)

    def on_mqtt_message(self, msg):
        print('Module ' + self.id + ": start sending mqtt")
        pass

    def on_websocket_message(self, msg):
        print('Module ' + self.id + ": start sending websocket")
        pass

    def get_time(self):
        now = datetime.datetime.now()
        reply = f"Právě je {now.hour} hodin {now.minute} minut a {now.second} sekund"
        print("Sending current time - " + reply)
        self.reply(reply)

    def get_day(self):
        now = datetime.datetime.now()
        reply = f"Dnes je {now.day}. {now.month}. {now.year}"
        print("Sending current day - " + reply)
        self.reply(reply)
        
    def set_timer(self):
        def play_timer_alarm():
            self.reply("čas vypršel") 

        time = 10
        print(f"Setting timer on {time} second")
        self.timer = threading.Timer(time, play_timer_alarm) 
        self.timer.start() 
        self.reply("nastavila jsem časovač na 10 sekund") 



    def play_timer_alarm(self):
        self.reply("Halóóó halóóó! čas vypršel") 

    def stop_timer(self):
        print("Timer is stopped.")
        self.timer.cancel()
        self.reply("vypnula jsem časovač") 