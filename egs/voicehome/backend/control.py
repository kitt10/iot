import socket


class VoicehomeControlInterface:

    def __init__(self, engine):
        self.engine = engine
        self.cfg = engine.cfg

        self.sock = None
        self.controller = None
        self.controller_id = ''
        self.disconnected = False
        self.commands = []
        self.replies = []

    def wait_for_controller(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        if command:
            if 'controller_handshake_id' in command:
                self.controller_id = command.split('_')[3]
                self.engine.webserver.packet['controller_id'] = self.controller_id

                # Send to web...
                ws_msg = {'passport': 'controller_connected',
                          'message': 'controller',
                          'controller_id': self.controller_id}
                self.engine.webserver.app.ws_message(ws_msg)
                return

            self.commands.append(command)
            print('Control: New command:', self.last_command())
            if self.last_command() == 'exit':
                self.disconnect_controller()
            if self.last_command() == 'temperature':
                query = {'key': 'voicehome/sensors/temperature'}
                res = self.search_mongo(self.id, query)
                print("res = ")
                print(res)

            # Pass the command to the logic
            self.engine.logic.on_command(command)

            # Pass the command to the web
            ws_msg = {'passport': 'communication',
                      'message': command,
                      'source': self.controller_id,
                      'IP': self.controller.getsockname()}
            self.engine.webserver.app.ws_message(ws_msg)

        else:
            self.disconnect_controller()
            self.restart_listening()

    def new_reply(self, reply):
        self.controller.sendall(str.encode(reply))
        self.replies.append(reply)
        print('Control: New reply:', self.last_reply())
        if self.last_reply() == 'exit':
            self.disconnect_controller()

        # Pass the reply to the web
        ws_msg = {'passport': 'communication',
                  'message': reply,
                  'source': 'engine',
                  'module_name': 'system'}  # TODO: module sending this reply...
        self.engine.webserver.app.ws_message(ws_msg)

    def disconnect_controller(self):
        self.disconnected = True
        print('Control: Controller disconnected from', self.controller.getsockname())

        # Send to web...
        ws_msg = {'passport': 'controller_disconnected',
                  'message': 'controller',
                  'controller_id': self.controller_id}
        self.engine.webserver.app.ws_message(ws_msg)
        self.engine.webserver.packet['controller_id'] = 'none'

        self.controller.close()
        self.sock.close()

    def restart_listening(self):
        self.disconnected = False
        self.wait_for_controller()

