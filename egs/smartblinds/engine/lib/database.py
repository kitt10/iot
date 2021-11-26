

class Database:
    
    def __init__(self, app):
        self.app = app
        self.cfg = app.cfg
        
    def get_data(self, limit=0):
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