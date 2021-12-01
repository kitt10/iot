from .cl_ifelse import CL_Ifelse
from .cl_ffnn import CL_Ffnn
from .cl_lstm import CL_Lstm
from time import time

class Classification:
    
    def __init__(self, app):
        self.app = app
        self.cfg = app.cfg
        
        self.classifiers = {
            'ifelse': CL_Ifelse(app=self.app),
            'ffnn': CL_Ffnn(app=self.app),
            'lstm': CL_Lstm(app=self.app)
        }
        
    def get_control(self, classifier_name, features):
        cl = self.classifiers[classifier_name]
        t0 = time()
        targets = cl.control(features)
        cl.control_time = time() - t0
        
        return {'status': 'ok', 'targets': targets, 'controlTime': cl.control_time}
    
    def do_train(self, classifier_name, data):
        cl = self.classifiers[classifier_name]
        if cl.trainable:
            t0 = time()
            cl.train(data)
            cl.last_trained = time()
            cl.train_time = cl.last_trained - t0
            
            return {'status': 'ok', 'trainTime': cl.train_time, 'lastTrained': cl.last_trained, 'nSamples': len(data)}
        else:
            return {'status': 'bad'}
        