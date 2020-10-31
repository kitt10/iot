import socket


class VoicehomeControlInterface:

    def __init__(self, engine):
        self.engine = engine
        self.cfg = engine.cfg

        self.sock = None
        self.controller = None
        self.disconnected = False
        self.commands = []
        self.replies = []

    def wait_for_controller(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.cfg.socket.host, self.cfg.socket.port))
        print('Control: Initialized. Listening on', self.cfg.socket.port)
        self.sock.listen()
        self.controller, _ = self.sock.accept()
        print('Control: Controller connected from', self.controller.getsockname())
        self.wait_for_commands()

    def wait_for_commands(self):
        while not self.disconnected:
            self.new_command(self.controller.recv(1024).decode())

        self.restart_listening()

    def last_command(self):
        return self.commands[-1]

    def last_reply(self):
        return self.replies[-1]

    def new_command(self, command):
        self.commands.append(command)
        print('Control: New command:', self.last_command())
        if self.last_command() == 'disconnect_controller':
            self.disconnect_controller()

        # Pass the command to the logic
        self.engine.logic.on_command(command)

    def new_reply(self, reply):
        self.controller.sendall(str.encode(reply))
        self.replies.append(reply)
        print('Control: New reply:', self.last_reply())
        if self.last_reply() == 'disconnect_controller':
            self.disconnect_controller()

    def disconnect_controller(self):
        self.disconnected = True
        print('Control: Controller disconnected from', self.controller.getsockname())
        self.controller.close()
        self.sock.close()

    def restart_listening(self):
        self.disconnected = False
        self.wait_for_controller()

