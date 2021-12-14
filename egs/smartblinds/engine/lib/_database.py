import numpy as np


def generate_toy_data():
    return [
        {
            "timestamp": 1637933115.62,
            "testing": False,   
            "periodical": False,
            "features": {
                "year_day": 212,
                "week_day": 4,
                "day_secs": 2321,
                "home": False,
                "temp_in": 23.42,
                "temp_out": 2.81,
                "lum_in": 231,
                "lum_out": 4783,
                "owm_temp_max": 4.1,
                "owm_temp_1h": 3,
                "owm_temp_2h": 2.2,
                "owm_temp_3h": 0,
                "owm_code": 804,
                "owm_wind_speed": 22,
                "owm_wind_heading": 23
            },
            "targets": {
                "position": 43,         
                "tilt": 23
            }
        },
        {
            "timestamp": 1637933134.62,
            "testing": True,   
            "periodical": False,
            "features": {
                "year_day": 212,
                "week_day": 4,
                "day_secs": 2342,
                "home": False,
                "temp_in": 23.42,
                "temp_out": 2.81,
                "lum_in": 143,
                "lum_out": 7866,
                "owm_temp_max": 4.1,
                "owm_temp_1h": 3,
                "owm_temp_2h": 2.2,
                "owm_temp_3h": 0,
                "owm_code": 804,
                "owm_wind_speed": 22,
                "owm_wind_heading": 23
            },
            "targets": {
                "position": 100,         
                "tilt": 0
            }
        },
        {
            "timestamp": 1637933215.62,
            "testing": False,   
            "periodical": True,
            "features": {
                "year_day": 212,
                "week_day": 4,
                "day_secs": 2421,
                "home": False,
                "temp_in": 24,
                "temp_out": 2.4,
                "lum_in": 6788,
                "lum_out": 3483,
                "owm_temp_max": 4.1,
                "owm_temp_1h": 3,
                "owm_temp_2h": 2.2,
                "owm_temp_3h": 0,
                "owm_code": 804,
                "owm_wind_speed": 22,
                "owm_wind_heading": 23
            },
            "targets": {
                "position": 69,         
                "tilt": 87
            }
        }
    ]
        
        
def generate_random_data(days=2):
    now = int(time())
    t_back = days*24*60*60
    samples = []
    for t in range(now-t_back, now):
        if t % 300 == 0:
            try:
                samples.append(self.random_sample(t, periodical=True, last_targets=samples[-1]['targets']))
            except IndexError:
                samples.append(self.random_sample(t, periodical=True))
        elif np.random.choice(list(range(1000))) == 0:
            samples.append(self.random_sample(t, periodical=False))
    
    print('FAKDB LOG: Generated '+str(len(samples))+' samples.')
    return samples
            
            
def random_sample(t, periodical, last_targets=None):
    dt = datetime.fromtimestamp(t)
    return {
            "timestamp": t,
            "testing": False,   
            "periodical": periodical,
            "features": {
                "year_day": int(dt.timetuple().tm_yday),
                "week_day": int(dt.weekday()),
                "day_secs": int((dt - dt.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()),
                "home": bool(np.random.choice([True, False])),
                "temp_in": float(np.random.choice(list(range(-20, 51)))),
                "temp_out": float(np.random.choice(list(range(-20, 51)))),
                "lum_in": float(np.random.choice(list(range(0, 10001)))),
                "lum_out": float(np.random.choice(list(range(0, 10001)))),
                "owm_temp_max": float(np.random.choice(list(range(-20, 51)))),
                "owm_temp_1h": float(np.random.choice(list(range(-20, 51)))),
                "owm_temp_2h": float(np.random.choice(list(range(-20, 51)))),
                "owm_temp_3h": float(np.random.choice(list(range(-20, 51)))),
                "owm_code": int(np.random.choice(list(range(200, 805)))),
                "owm_wind_speed": float(np.random.choice(list(range(0, 51)))),
                "owm_wind_heading": float(np.random.choice(list(range(0, 360))))
            },
            "targets": {
                "position": last_targets['position'] if last_targets else int(np.random.choice(list(range(0, 101)))),         
                "tilt": last_targets['tilt'] if last_targets else int(np.random.choice(list(range(0, 101))))
            }
        }