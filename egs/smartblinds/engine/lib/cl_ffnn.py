from ._classification import Classifier
import numpy as np
from ._tools import make_vector

class CL_Ffnn(Classifier):
    
    def __init__(self, app):
        Classifier.__init__(self, app, 'ffnn', True, ind=1)

    def control(self, features):
        
        X = np.array([self.make_vector(features, self.taskF)])
        U = self.model.predict(X)

        position = round(float(U[0][0]), 2)*100
        tilt = round(float(U[0][1]), 2)*100

        print('X:', X)
        print('U:', U)
        print('suggested position / tilt:', position, tilt)
            
        return position, tilt
    
    def train(self, data):
        self.app.cl.log('Training classifier '+self.name)
        pass

    def predict(self, data):
        X = np.array([make_vector(item['features'], self.taskF) for item in data])
        predictions = self.model.predict(X)*100
        timestamps = np.array([item['timestamp'] for item in data])
        return timestamps, predictions