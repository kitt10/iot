
class CL_Ifelse:
    
    def __init__(self, app):
        self.app = app
        self.trainable = False
        
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

