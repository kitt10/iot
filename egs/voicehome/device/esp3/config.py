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
    QUANTITY_ILLUMINANCE = 'lux',
    QUANTITY_PRESSURE = 'hPa',
    QUANTITY_TEMPERATURE = 'degrees',
    QUANTITY_HUMIDITY = 'percent',
    TOPIC_ILLUMINANCE = 'voicehome/sensors/illuminance',
    TOPIC_PRESSURE = 'voicehome/sensors/pressure',
    TOPIC_TEMPERATURE = 'voicehome/sensors/temperature',
    TOPIC_HUMIDITY = 'voicehome/sensors/humidity',
    TOPIC_SUBSCRIBE_LIGHTS='voicehome/lights/command',
    TOPIC_SUBSCRIBE_COMMAND='voicehome/sensors/commands',
    KEEPALIVE = 60,
    PORT = 1883)