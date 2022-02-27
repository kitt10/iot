from ._classification import Classifier
import numpy as np

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

    def make_vector(self, data, taskInfo):
        return [norm(data[name], *info) for name, info in taskInfo.items()]

# should not be in this file...
def norm(value, a_type, a_min, a_max):
    if a_type == 'boolean':
        return int(value)
    else:
        return (value-a_min)/(a_max-a_min)