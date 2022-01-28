from ._classification import Classifier
from keras.models import load_model
import numpy as np

class CL_Ffnn(Classifier):
    
    def __init__(self, app):
        Classifier.__init__(self, app, 'ffnn', ind=1)
        self.trainable = True

        # Load trained model
        self.model = load_model(app.cfg['classification']['ffnn_model'])
        self.app.cl.log('FFNN model loaded.')
        self.model.summary()

    def control(self, features):
        print('features:', features)
        print(self.model.predict(np.array(features)))

        position = np.random.randint(0, 100)    # TODO
        tilt = np.random.randint(0, 100)        # TODO
            
        return position, tilt
    
    def train(self, data):
        self.app.cl.log('Training classifier '+self.name)
        pass

