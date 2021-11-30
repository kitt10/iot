from lib._tools import *
from lib.database import Database
from lib.classification import Classification
from lib.webserver import WebServer

class App:
    
    def __init__(self, cfg_file):
        
        # Load config
        self.cfg_file = cfg_file
        self.cfg = load_config(self.cfg_file)
        
        # Load task
        self.task = load_task(self.cfg)
        
        # Init App
        self.name = self.cfg['app']['name']
        self.description = self.cfg['app']['description']
        
        # Init Database
        self.db = Database(app=self)
        
        # Init Classifiers
        self.cl = Classification(app=self)
        
        # Init API WebServer
        self.ws = WebServer(app=self)
        
        # Run API WebServer
        self.ws.run()


if __name__ == '__main__':
    App(cfg_file='cfg_engine.yml')
    