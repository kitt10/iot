import socket


class ControlInterface:

    def __init__(self, engine):
        self.engine = engine
        self.cfg = engine.cfg

        self.controller = None
        self.controller_addr = None
        self.control_commands = []

    def wait_for_controller(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.cfg.socket.host, self.cfg.socket.port))
            print('Control: Initialized. Listening on', self.cfg.socket.port)
            sock.listen()
            self.controller, self.controller_addr = sock.accept()
            self.control_loop()

    def control_loop(self):
        print('Control: New connection from', self.controller_addr)
        while True:
            self.control_commands.append(self.controller.recv(1024))
            if self.last() == 'disconnect_controller':
                self.controller.close()
                break

            print('Control: New command:', self.last())

    def last(self):
        return self.control_commands[-1]

