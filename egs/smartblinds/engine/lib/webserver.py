from tornado.web import Application, StaticFileHandler
from tornado.ioloop import IOLoop
import datetime
from os.path import join, dirname
from .ep_web import EP_Web
from .ep_data import EP_Data
from .ep_control import EP_Control
from .ep_train import EP_Train

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
                     ('/ep_control/', EP_Control, {'app': self.app}),
                     ('/ep_train/', EP_Train, {'app': self.app}),
                     ('/(.*)', StaticFileHandler, {'path': self.static_path_abs})
                    ]

        settings = {
                'debug': self.debug, 
                'autoreload': self.debug}

        self.tornado_app = Application(endpoints, **settings)
        self.tornado_app.listen(self.port)
        self.current_loop = IOLoop.current()
    
    def plan_next_training(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        midnight = datetime.datetime.combine(tomorrow, datetime.time.min)
        self.current_loop.add_timeout(midnight-datetime.datetime.now(), self.app.cl.retrain_all)
        self.app.cl.set_next_training(midnight.strftime('%d.%m.%Y %H:%M:%S'))
        self.log('Next classifiers training planned to: '+self.app.cl.next_training)
        
    def run(self):
        self.log('Starting '+self.app.name+', port: '+str(self.port))
        self.current_loop.start()

    def log(self, buf):
        if self.verbose:
            print(datetime.datetime.now(), 'SERVER LOG:', buf)