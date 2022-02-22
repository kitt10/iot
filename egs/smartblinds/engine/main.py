# Force use CPU (should work as well and will not block other KKY-PC GPU processes)
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'        # shut up tensorflow debug messages
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = ""

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
        
        # Plan Classifiers Trainings to every midnight
        self.ws.plan_next_training()
        
        # Run API WebServer
        self.ws.run()


if __name__ == '__main__':
    App(cfg_file='cfg_engine.yml')
    