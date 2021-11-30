from .cl_ifelse import CL_Ifelse
from .cl_ffnn import CL_Ffnn
from .cl_lstm import CL_Lstm

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
        return self.classifiers[classifier_name].control(features)
        