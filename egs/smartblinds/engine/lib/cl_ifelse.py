from ._classification import Classifier
import pysolar
import datetime as dt
import math
from ._tools import trim, load_config
import numpy as np

class CL_Ifelse(Classifier):
    
    def __init__(self, app):
        Classifier.__init__(self, app, 'ifelse', False, ind=0)
        self.cfg = load_config("./lib/cfg_ifelse.yml")
        
    def control(self, features):        
        if 21600 < features['day_secs'] < 61200:
            pos, tilt = self.__light(features)
        else:
            pos, tilt = self.__dark(features)
        return trim(pos), trim(tilt)

    def predict(self, data):
        predictions = np.array([list(self.control(item['features'])) for item in data])
        timestamps = np.array([item['timestamp'] for item in data])
        return timestamps, predictions

    def __light(self, features):
        def open(features = features):
            return 100, 100
        def tilt(features = features):
            c = 1
            if not features['home']:
                c = self.cfg['away_tilt_coef']
            return 0, c*self.__suntilt(features)
        def close(features = features):
            return 0, 100
        def tilt_or_open(features=features):
            azimuth, altitude = pysolar.solar.get_position(self.app.cfg['blind']['lat'], self.app.cfg['blind']['lon'], dt.datetime(dt.datetime.now().year, 1, 1, tzinfo = dt.timezone.utc) + dt.timedelta(days = features['year_day'] - 1, seconds = features['day_secs']))
            az_diff = (azimuth - self.app.cfg['blind']['azimuth'] + 180) % 360 - 180
            if az_diff>90:
                return open()
            return tilt()

        season = self.__season_value(features)
        if season == 2:
            return tilt()
        elif season == 1:
            grad = features['temp_owm_2h'] - features['temp_owm_1h']
            if features['temp_out'] < self.cfg['temp_out_thresholds']['cold']:
                return open()
            elif features['temp_out'] < self.cfg['temp_out_thresholds']['mid']:
                if grad > self.cfg['temp_grad_thresholds']['pos']:
                    return tilt_or_open()
                elif grad < self.cfg['temp_grad_thresholds']['neg']:
                    return open()
                else:
                    return close()
            else:
                return tilt_or_open()
        else:
            return 100, 100

    def __dark(self, features):
        if features['home'] and features['day_secs'] > 79200 or features['temp_in'] < self.cfg['temp_in_thresholds']['ventilation']:
            return 0, 28
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

    def __temperature_value(self, features):
        val = 0
        rate = self.__temperature_rate(features)

        if features['temp_in'] < self.cfg['temp_in_thresholds']['cold']: val -= 2
        elif features['temp_in'] > self.cfg['temp_in_thresholds']['mid']: val += 2

        if features['temp_out'] < self.cfg['temp_out_thresholds']['cold']: val -= 1
        elif features['temp_out'] > self.cfg['temp_out_thresholds']['mid']: val += 1
        else:
            if rate > self.cfg['temp_grad_thresholds']['pos']: val += 1
            elif rate < self.cfg['temp_grad_thresholds']['neg']: val -= 1

    def __temperature_rate(self, features):
        w1 = 2
        w2 = 1

        return ((features['temp_owm_2h'] - features['temp_owm_1h'])*w1 + (features['temp_owm_3h'] - features['temp_owm_2h'])*w2)/(w1+w2)

    def __season_value(self, features):
        if features['year_day'] < 80 or features['year_day'] >= 321: 
            return 0
        val = 1
        if features['year_day'] > 135 and features['year_day'] < 274:
            val += 1
        return val
        

