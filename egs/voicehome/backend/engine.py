from sys import version as py_version
from argparse import ArgumentParser
from threading import Thread, ThreadError
from box import Box

from mqtt_client import VoicehomeMQTTClient
from webserver import VoicehomeWebserver


class Engine:

    def __init__(self):

        # Parse args and load config
        self.args = None
        self.cfg = None
        self.args_and_config()

        # MQTT Client (new thread)
        self.mqtt = None
        self.mqtt_thread(daemonic=False)

        # Tornado Webserver (new thread)
        self.webserver = None
        self.webserver_thread(daemonic=False)

        # Mongo Database

        # VoiceKit Interface

        # Modules

    def args_and_config(self):
        parser = ArgumentParser(description='Voicehome engine.')
        parser.add_argument('-c', '--cfg_path', type=str, default='config.yml', help='Path to the config file.')
        self.args = parser.parse_args()
        self.cfg = Box.from_yaml(filename=self.args.cfg_path)

        print(py_version, 'Config file:', self.args.cfg_path)
        print('------------------------------------------------')

    def mqtt_thread(self, daemonic=False):
        self.mqtt = VoicehomeMQTTClient(engine=self)
        try:
            t = Thread(target=self.mqtt.loop_forever)
            t.setDaemon(daemonic)
            t.start()
        except ThreadError:
            print('ERR: Thread MQTT.')

    def webserver_thread(self, daemonic=False):
        self.webserver = VoicehomeWebserver(engine=self)
        try:
            t = Thread(target=self.webserver.iol.start)
            t.setDaemon(daemonic)
            t.start()
        except ThreadError:
            print('ERR: Thread Webserver.')


if __name__ == '__main__':
    Engine()
