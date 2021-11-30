import numpy as np

class CL_Ffnn:
    
    def __init__(self, app):
        self.app = app
        self.trainable = True
        
    def control(self, features):
        position = np.random.randint(0, 100)    # TODO
        tilt = np.random.randint(0, 100)        # TODO
            
        return position, tilt

