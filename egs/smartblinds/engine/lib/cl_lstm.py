from ._classification import Classifier
import numpy as np
from ._tools import make_matrix

class CL_Lstm(Classifier):
    
    def __init__(self, app):
        Classifier.__init__(self, app, 'lstm', True, ind=2)
        
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

    def predict(self, data):
        t = self.timesteps
        k = len(data) - t

        X = np.array([make_matrix(data[i:i+t], 'features', self.taskF) for i in range(k)])
        predictions = 100*self.model.predict(X, batch_size=1)
        timestamps = np.array([data[i+t-1]['timestamp'] for i in range(k)])
        return timestamps, predictions

    @property
    def timesteps(self):
        return self.model.get_config()["layers"][0]["config"]["batch_input_shape"][1]

