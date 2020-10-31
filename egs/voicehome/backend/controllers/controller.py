from sys import version as py_version
from argparse import ArgumentParser
from box import Box
from threading import Thread, ThreadError
import socket


class VoicehomeController:

    def __init__(self):

        # Parse args and load config
        self.args = None
        self.cfg = None
        self.args_and_config()

        self.sock = None
        self.disconnected = False
        self.replies = []
        self.commands = []

        try:
            t = Thread(target=self.connect_and_listen)
            t.setDaemon(False)
            t.start()
        except ThreadError:
            print('ERR: Thread Controller Listener.')

    def args_and_config(self):
        parser = ArgumentParser(description='Voicehome controller.')
        parser.add_argument('-c', '--cfg_path', type=str, default='../config.yml', help='Path to the config file.')
        self.args = parser.parse_args()
        self.cfg = Box.from_yaml(filename=self.args.cfg_path)

        print(py_version, 'Config file:', self.args.cfg_path)
        print('------------------------------------------------')

    def connect_and_listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.cfg.socket.host, self.cfg.socket.port))

        while not self.disconnected:
            try:
                self.replies.append(self.sock.recv(1024).decode())
                self.new_reply()
            except OSError:
                pass

    def last_reply(self):
        return self.replies[-1]

    def last_command(self):
        return self.commands[-1]

    def new_reply(self):
        if self.last_reply() == 'disconnect_controller':
            self.disconnect_controller()

        print('Got new reply:', self.last_reply())

    def new_command(self, command):
        self.commands.append(command)
        self.sock.sendall(str.encode(command))
        if self.last_command() == 'disconnect_controller':
            self.disconnect_controller()

    def disconnect_controller(self):
        self.disconnected = True
        self.sock.close()
        print('Controller disconnected.')
