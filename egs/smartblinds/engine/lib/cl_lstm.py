from ._classification import Classifier
import numpy as np

class CL_Lstm(Classifier):
    
    def __init__(self, app):
        Classifier.__init__(self, app, 'lstm', ind=2)
        self.trainable = True
        
    def control(self, features):
        position = np.random.randint(0, 100)    # TODO
        tilt = np.random.randint(0, 100)        # TODO
            
        return position, tilt
    
    def train(self, data):
        self.app.cl.log('Training classifier '+self.name)

