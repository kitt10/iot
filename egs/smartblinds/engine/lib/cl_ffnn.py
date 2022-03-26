from ._classification import Classifier
import numpy as np
from ._tools import make_vector

class CL_Ffnn(Classifier):
    
    def __init__(self, app):
        Classifier.__init__(self, app, 'ffnn', True, ind=1)

    def control(self, features):
        
        X = np.array([make_vector(features, self.taskF)])
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
        l = X.shape[0]
        model_cfg = self.model.get_config()
        for i in range(2):
            model_cfg['layers'][i]['config']['batch_input_shape'] = (l,len(self.taskF))
        new_model = self.model.__class__.from_config(model_cfg)
        new_model.set_weights(self.model.get_weights())

        predictions = new_model.predict(X, batch_size=l)*100
        timestamps = np.array([item['timestamp'] for item in data])
        return timestamps, predictions