from tornado.web import Application, StaticFileHandler
from tornado.ioloop import IOLoop
from os.path import join, dirname
from .ep_web import EP_Web
from .ep_data import EP_Data

class WebServer:
    
    def __init__(self, app):
        self.app = app
        self.cfg = app.cfg
        self.port = self.cfg['webserver']['port']
        self.static_path_rel = self.cfg['webserver']['static_path_rel']
        self.static_path_abs = join(dirname(__file__), self.static_path_rel)
        self.static_index = self.cfg['webserver']['static_index']
        self.host_web = self.cfg['webserver']['host_web']
        self.verbose = self.cfg['webserver']['verbose']
        self.debug = self.cfg['webserver']['debug']

        endpoints = [('/', EP_Web, {'webserver': self}),
                     ('/ep_data/', EP_Data, {'app': self.app}),
                     ('/(.*)', StaticFileHandler, {'path': self.static_path_abs})
                    ]

        settings = {
                'debug': self.debug, 
                'autoreload': self.debug}

        app = Application(endpoints, **settings)
        app.listen(self.port)
        
    def run(self):
        self.log('Starting '+self.app.name+', port: '+str(self.port))
        IOLoop.current().start()

    def log(self, buf):
        if self.verbose:
            print('SERVER LOG:', buf)