## Smartblinds: Scripts

### broker2mongo.py

This script subscribes to the MQTT broker and saves published data to a MONGO database.

#### cfg_broker2mongo.yml
```yaml
broker:
  host:                     # string
  port:                     # number
  uname:                    # string
  passwd:                   # string
  topic: 'smartblinds/data' # string
  verbose: false            # boolean
mongo:
  host:                     # string
  port:                     # number
  database: 'smartblinds'   # string
  collection: 'data'        # string [real / sim]
  verbose: true             # boolean
verbose: true               # boolean
```

#### MQTT Topic
```json
smartblinds/data
```

#### MQTT Message
```json
{
  "timestamp": ,          // float (seconds since 1.1.1970)
  "testing": ,            // boolean (testing mode)
  "features": {
    "year_day": ,         // int <1, 365>
    "week_day": ,         // int <0, 6>
    "day_secs": ,         // int <0, 86400>
    "home": ,             // int {0, 1}
    "temp_in": ,          // float <-30, 50>
    "temp_out": ,         // float <-30, 50>
    "lum_in": ,           // float <0, 10000>
    "lum_out": ,          // float <0, 10000>
    "owm_temp_max": ,     // float <-30, 50>
    "owm_temp_1h": ,      // float <-30, 50>
    "owm_temp_2h": ,      // float <-30, 50>
    "owm_temp_3h": ,      // float <-30, 50>
    "owm_code": ,         // int <200, 804> ?!
    "owm_wind_speed": ,   // float <0, 50>
    "owm_wind_heading": , // float <0, 359>
  },
  "targets": {
    "position": ,         // int <0, 100>
    "tilt": ,             // int <0, 100>
  }
}
```

---

### owm2mqtt.py