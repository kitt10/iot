from sys import version as py_version
from argparse import ArgumentParser
from box import Box
from threading import Thread, ThreadError
from abc import abstractmethod
import os
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

        self.controller_id = ''

        try:
            t = Thread(target=self.connect_and_listen)
            t.setDaemon(False)
            t.start()
        except ThreadError:
            print('ERR: Thread Controller Listener.')

    def args_and_config(self):
        cfg_path = '../config.yml'
        self.cfg = Box.from_yaml(filename=cfg_path)
        parser = ArgumentParser(description='Voicehome controller.', add_help=False)
        parser.add_argument('-h', '--host', type=str, default=self.cfg.socket.host, help='Destination system IP.')
        parser.add_argument('-p', '--port', type=int, default=self.cfg.socket.port, help='Destination system port.')
        self.args = parser.parse_args()

        print(py_version, 'Config file:', cfg_path)
        print('------------------------------------------------')

    def connect_and_listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.args.host, self.args.port))

        # handshake - log self
        self.sock.sendall(str.encode('controller_handshake_id_'+self.controller_id))

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
        if self.last_reply():
            if self.last_reply() == 'exit':
                self.disconnect_controller()

            self.got_reply(self.last_reply())
        else:
            self.disconnect_controller()

    def new_command(self, command):
        self.commands.append(command)
        self.sock.sendall(str.encode(command))
        if self.last_command() == 'exit':
            self.disconnect_controller()

    def disconnect_controller(self):
        self.disconnected = True
        self.sock.close()
        print('Controller disconnected.')
        os._exit(0)

    @abstractmethod
    def got_reply(self, reply):
        pass
