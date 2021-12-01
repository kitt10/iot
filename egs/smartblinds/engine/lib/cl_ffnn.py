from ._classification import Classifier
import numpy as np

class CL_Ffnn(Classifier):
    
    def __init__(self, app):
        Classifier.__init__(self, app, 'ffnn')
        self.trainable = True
        
    def control(self, features):
        position = np.random.randint(0, 100)    # TODO
        tilt = np.random.randint(0, 100)        # TODO
            
        return position, tilt
    
    def train(self, data):
        pass

