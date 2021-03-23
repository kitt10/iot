from modules.voicehome_module import VoicehomeModule
import datetime
import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

class Time(VoicehomeModule):

    def __init__(self, engine, dir_path, active):
        VoicehomeModule.__init__(self, engine, dir_path, active)

        options = Options()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')

        self.driver = webdriver.Chrome(executable_path=engine.cfg.chromedriver.path,chrome_options=options)

        self.URL_sunset_sunrise = 'https://www.meteogram.cz/vychod-zapad-slunce/'
        self.URL_namedays = 'http://svatky.centrum.cz/'

        self.regex_pattern_sunrise = 'VÝCHOD SLUNCE '
        self.regex_pattern_sunset = 'ZÁPAD SLUNCE '

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
        self.reply("Časovač je nastaven na 10 sekund")



    def play_timer_alarm(self):
        self.reply("Halóóó halóóó! čas vypršel") 

    def stop_timer(self):
        print("Timer is stopped.")
        self.timer.cancel()
        self.reply("vypnula jsem časovač")

    def get_weekday(self):
        weekday = datetime.date.today().weekday()
        if (weekday == 0):
            self.reply('Dnes je pondělí')
        elif (weekday == 1):
            self.reply('Dnes je úterý')
        elif (weekday == 2):
            self.reply('Dnes je středa')
        elif (weekday == 3):
            self.reply('Dnes je čtvrtek')
        elif (weekday == 4):
            self.reply('Dnes je pátek')
        elif (weekday == 5):
            self.reply('Dnes je sobota')
        elif (weekday == 6):
            self.reply('Dnes je neděle')

    def get_sunrise_time(self):
        try:
            self.driver.get(self.URL_sunset_sunrise)
            results = self.driver.find_element_by_id('suntable').text.split('\n')
        except:
            results = ''
            pass

        if results == '':
            self.reply('Nebylo možno získat data ze serveru meteogram.cz')
            return

        for line in results:
            match = re.search('^(' + self.regex_pattern_sunrise + ')', line)
            if match:
                result = match.string.replace(self.regex_pattern_sunrise, "").split(":")
                hour = result[0]
                if hour[0]=='0':
                    hour = hour[1]

                minute = result[1]
                if minute[0]=='0':
                    minute=minute[1]
                break

        else:
            self.reply('Nebylo možno získat data ze serveru meteogram.cz')
            return

        self.reply('Slunce vychází v ' + hour + " hodin a " + minute + ' minut.')

    def get_sunset_time(self):
        try:
            self.driver.get(self.URL_sunset_sunrise)
            results = self.driver.find_element_by_id('suntable').text.split('\n')
        except:
            results = ''
            pass

        if results == '':
            self.reply('Nebylo možno získat data ze serveru meteogram.cz')
            return

        for line in results:
            match = re.search('^(' + self.regex_pattern_sunset + ')', line)
            if match:
                result = match.string.replace(self.regex_pattern_sunset, "").split(":")
                hour = result[0]
                if hour[0] == '0':
                    hour = hour[1]

                minute = result[1]
                if minute[0] == '0':
                    minute = minute[1]
                break

        else:
            self.reply('Nebylo možno získat data ze serveru meteogram.cz')
            return

        self.reply('Slunce zapadá v ' + hour + " hodin a " + minute + ' minut.')

    def get_nameday(self):
        try:
            self.driver.get(self.URL_namedays)
            nameday = self.driver.find_element_by_id('holiday').text.replace(':','')
        except:
            nameday = ''
            pass

        if nameday == '':
            self.reply('Nebylo možno získat data ze serveru svatky.centrum.cz')
            return

        self.reply('Podle serveru svatky.centrum.cz '+nameday)