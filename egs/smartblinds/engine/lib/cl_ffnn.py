from ._classification import Classifier
from keras.models import load_model
from collections import OrderedDict
import numpy as np

class CL_Ffnn(Classifier):
    
    def __init__(self, app):
        Classifier.__init__(self, app, 'ffnn', ind=1)
        self.trainable = True

        # Load trained model
        self.model = load_model(app.cfg['classification']['ffnn_model'])
        print('FFNN model loaded.')
        self.model.summary()

        # Prepare env
        self.taskF = OrderedDict()
        self.taskT = OrderedDict()
        self.get_task_info()

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

    def get_task_info(self):
        for feature in self.app.task['features']:
            self.taskF[feature['name']] = (feature['type'], feature['min'], feature['max'])

        for target in self.app.task['targets']:
            self.taskT[target['name']] = (target['type'], target['min'], target['max'])

    def make_vector(self, data, taskInfo):
        return [norm(data[name], *info) for name, info in taskInfo.items()]

# should not be in this file...
def norm(value, a_type, a_min, a_max):
    if a_type == 'boolean':
        return int(value)
    else:
        return (value-a_min)/(a_max-a_min)