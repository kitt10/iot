#CONFIGURATION FILE WITH PARAMETERS

PARAMS = dict(
    ENABLE_EXTERNAL_LED = True,
    ENABLE_INTERNAL_LED = True)

GPIO = dict(
    EXTERNAL_LED = 13,
    TSL_SCL = 5,
    TSL_SDA = 4)    

WIFI = dict(
    SSID = 'HP Deskjet 2720 All-in-One',
    PASSWD = 'PodlahajehnedaStropjebily730')

MQTT = dict(
    ESP_ID=3,
    LightsID=[],
    SERVER = '147.228.124.230',
    USER = 'sanda', 
    PASSWD = 'denmark',
    SENSOR_ID = 'tsl2591_1',
    LOCATION = 'room_1',
    OWNER = 'jsanda',
    QUANTITY_UNITS_ILLUMINANCE='lx',
    QUANTITY_TYPE_ILLUMINANCE='illuminance',
    TOPIC_ILLUMINANCE = 'voicehome/sensors/illuminance',
    TOPIC_SUBSCRIBE_LIGHTS='voicehome/lights/command',
    TOPIC_SUBSCRIBE_LIGHTS_STATE='voicehome/lights/state/command',
    TOPIC_LIGHTS_STATE='voicehome/lights/state/receive',
    TOPIC_MEASURE_COMMAND='voicehome/sensors/command',
    KEEPALIVE = 60,
    PORT = 1883)