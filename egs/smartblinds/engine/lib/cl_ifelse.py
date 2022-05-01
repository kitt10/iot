from ._classification import Classifier
import pysolar
import datetime as dt
import math
from ._tools import trim, load_config
import numpy as np
import os, sys
from keras.metrics import MeanSquaredError as MSE

class CL_Ifelse(Classifier):
    
    def __init__(self, app):
        Classifier.__init__(self, app, 'ifelse', False, ind=0)
        print(sys.path)
        self.cfg = load_config(os.path.join(sys.path[0],"..","engine","lib","cfg_ifelse.yml"))

    def control(self, features):        
        if self.cfg["morning_seconds"][features['week_day']] < features['day_secs'] and self.cfg["lum_thresholds"]['low']<features["lum_out"]:
            pos, tilt = self.__light(features)
        else:
            pos, tilt = self.__dark(features)
        return trim(pos), trim(tilt)

    def predict(self, data):
        predictions = np.array([list(self.control(item['features'])) for item in data])
        timestamps = np.array([item['timestamp'] for item in data])
        return timestamps, predictions

    def evaluate(self, X, Y, metrics):
        data = list()
        for row in X:
            data.append({"timestamp": None, "features": dict(zip([f["name"] for f in self.app.task["features"]], row))})
        ts, Y_hat = self.predict(data)
        results = list()
        for m in [MSE()] + metrics:
            results.append(m(Y, Y_hat).numpy())
        return results

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
            if az_diff>90 or features["owm_temp_max"] < self.cfg["temp_out_thresholds"]["mid"]:
                return open()
            return tilt()

        season = self.__season_value(features)
        if season == 2:
            if features["home"]: return tilt_or_open()
            return tilt()
        elif season == 1:
            grad = features['owm_temp_2h'] - features['owm_temp_1h']
            L = self.app.task["features"][2]["max"]
            gon = math.cos(math.pi*(features["day_secs"]-L/2)/L)
            h = gon*gon/L
            if features['temp_out'] < self.cfg['temp_out_thresholds']['cold']:
                return open()
            elif features['temp_out'] < self.cfg['temp_out_thresholds']['mid']:
                if grad > self.cfg['temp_grad_thresholds']['pos'] or features["lum_out"]/h>self.cfg['lum_thresholds']['high'] and features["temp_in"] > self.cfg['temp_in_thresholds']['mid']:
                    return tilt_or_open()
                elif grad < self.cfg['temp_grad_thresholds']['neg']:
                    return open()
                else:
                    return close()
            elif features["lum_out"]/h>self.cfg['lum_thresholds']['high']: 
                return tilt_or_open()
            else:
                close()
        else:
            return open()

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

        return ((features['owm_temp_2h'] - features['owm_temp_1h'])*w1 + (features['owm_temp_3h'] - features['owm_temp_2h'])*w2)/(w1+w2)

    def __season_value(self, features):
        if features['year_day'] < 80 or features['year_day'] >= 321: 
            return 0
        val = 1
        if features['year_day'] > 135 and features['year_day'] < 274:
            val += 1
        return val
        
    @property
    def batch_size(self):
        return 1
