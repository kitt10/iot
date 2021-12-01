from ._classification import Classifier

class CL_Ifelse(Classifier):
    
    def __init__(self, app):
        Classifier.__init__(self, app, 'ifelse', ind=0)
        self.trainable = True
        
    def control(self, features):
        position = 100
        tilt = 100
        
        if 21600 < features['day_secs'] < 61200:
            position = 0
            tilt = 35
            
        if features['temp_out'] < 35:
            position = 40
            tilt = 78
            
        return position, tilt

