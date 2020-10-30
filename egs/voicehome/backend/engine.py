from sys import version as py_version
from argparse import ArgumentParser
from config import Config
from .mqtt import VoicehomeMQTTClient


class Engine:

    def __init__(self):

        # Parse args and load config
        self.args = None
        self.cfg = None
        self.args_and_config()

        # MQTT Client (new thread)
        self.mqtt = VoicehomeMQTTClient(engine=self)

        # Tornado Webserver

        # Mongo Database

        # VoiceKit Interface

        # Modules

    def args_and_config(self):
        parser = ArgumentParser(description='Voicehome engine.')
        parser.add_argument('-c', '--cfg_path', type=str, default='config.cfg', help='Path to the config file.')
        self.args = parser.parse_args()

        print(py_version, 'Config file:', self.args.cfg_path)
        print('------------------------------------------------')
        with open(self.args.cfg_path, 'r') as f:
            self.cfg = Config(f)


if __name__ == '__main__':
    Engine()
