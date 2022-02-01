from ._classification import Classifier
import pysolar
import datetime as dt
import math
from ._tools import trim

class CL_Ifelse(Classifier):
    
    def __init__(self, app):
        Classifier.__init__(self, app, 'ifelse', ind=0)
        self.trainable = False
        self.app = app
        
    def control(self, features):        
        if 21600 < features['day_secs'] < 61200:
            pos, tilt = self.__light(features)
        else:
            pos, tilt = self.__dark(features)
        return trim(pos), trim(tilt)

    def __light(self, features):
        if self.__is_summer(features):
            return 0, self.__suntilt(features)
        else:
            return 100, 100

    def __dark(self, features):
        return 0, 0

    def __suntilt(self, features):
        azimuth, altitude = pysolar.solar.get_position(self.app.cfg['blind']['lat'], self.app.cfg['blind']['lon'], dt.datetime(dt.datetime.now().year, 1, 1, tzinfo = dt.timezone.utc) + dt.timedelta(days = features['year_day'] - 1, seconds = features['day_secs']))
        az_diff = abs((azimuth - self.app.cfg['blind']['azimuth'] + 180) % 360 - 180)
        if az_diff < 90:
            return (10 / 9
            * 1.5
            * math.degrees(math.atan(
                math.tan(math.radians(altitude)))
                / math.cos(math.radians(az_diff))
                )
            )
        else:
            return 100

    def __is_summer(self, features):
        return features['year_day'] > 110 and features['year_day'] < 270
        

