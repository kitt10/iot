from abc import ABC
from tornado.web import StaticFileHandler, RequestHandler as TornadoRequestHandler, Application as TornadoApplication
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from os.path import dirname, join as join_path
from json import dumps as dumps_json


class VoicehomeMainHandler(TornadoRequestHandler, ABC):

    @staticmethod
    def initialize():
        print('Webserver: New MainHandler.')

    def get(self):
        self.render(join_path(self.application.cfg.tornado.frontend_relative, self.application.cfg.tornado.index_page))


class VoicehomeWebSocketHandler(WebSocketHandler, ABC):

    def initialize(self):
        self.application.ws_clients.append(self)
        print('Webserver: New WS Client. Connected clients:', len(self.application.ws_clients))

    def open(self):
        print('Webserver: Websocket opened.')
        self.write_message('Server ready.')

    def on_message(self, message):
        print('Webserver: Received WS message:'+str(message))

    def on_close(self):
        self.application.ws_clients.remove(self)
        print('Webserver: Websocket client closed. Connected clients:', len(self.application.ws_clients))


class VoicehomeJsonHandler(TornadoRequestHandler, ABC):

    @staticmethod
    def initialize():
        print('Webserver: New JsonHandler')

    def get(self):
        self.write(dumps_json(self.application.packet))


class VoicehomeTornadoApp(TornadoApplication):

    def __init__(self, webserver):
        self.webserver = webserver
        self.cfg = webserver.cfg

        self.packet = {}
        self.ws_clients = []

        self.tornado_handlers = [
            (r'/', VoicehomeMainHandler),
            (r'/websocket', VoicehomeWebSocketHandler),
            (r'/packet', VoicehomeJsonHandler),
            (r'/(.*)', StaticFileHandler, {
                'path': join_path(dirname(__file__), self.cfg.tornado.frontend_relative)})
        ]
        self.tornado_settings = {
            "debug": self.cfg.tornado.debug,
            "autoreload": self.cfg.tornado.debug
        }
        TornadoApplication.__init__(self, self.tornado_handlers, **self.tornado_settings)

    def ws_message(self, message):
        for client in self.ws_clients:
            self.webserver.iol.spawn_callback(client.write_message, dumps_json(message))


class VoicehomeWebserver:

    def __init__(self, engine):
        self.engine = engine
        self.cfg = engine.cfg

        self.app = VoicehomeTornadoApp(webserver=self)
        self.app.listen(self.cfg.tornado.port)
        self.iol = IOLoop.current()
        print('Webserver: Initialized. Listening on', self.cfg.tornado.port)

    def run_loop(self):
        self.iol.start()