from tornado.web import StaticFileHandler, RequestHandler as TornadoRequestHandler, Application as TornadoApplication
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from os.path import dirname, join as join_path


class VoicehomeMainHandler(TornadoRequestHandler):

    def initialize(self):
        self.cfg = self.application.settings.get('cfg')

    def get(self):
        self.render(join_path(self.cfg.tornado.frontend_relative, self.cfg.tornado.index_page))

    def data_received(self):
        pass


class VoicehomeTornadoApp(TornadoApplication):

    def __init__(self, cfg):
        self.cfg = cfg
        self.tornado_handlers = [
            (r'/', VoicehomeMainHandler),
            (r'/(.*)', StaticFileHandler, {
                'path': join_path(dirname(__file__), self.cfg.tornado.frontend_relative)})
        ]
        self.tornado_settings = {
            "debug": self.cfg.tornado.debug,
            "autoreload": self.cfg.tornado.debug,
            "cfg": self.cfg
        }
        TornadoApplication.__init__(self, self.tornado_handlers, **self.tornado_settings)


class VoicehomeWebserver:

    def __init__(self, engine):
        self.engine = engine
        self.cfg = engine.cfg

        self.app = VoicehomeTornadoApp(self.cfg)
        self.app.listen(self.cfg.tornado.port)
        self.iol = IOLoop.current()
        print('Webserver: Initialized. Listening on', self.cfg.tornado.port)

    def run_loop(self):
        self.iol.start()
