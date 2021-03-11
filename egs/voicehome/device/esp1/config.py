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
    ESP_ID=1,
    LightsID=[],
    SERVER = '147.228.124.230',
    USER = 'sanda', 
    PASSWD = 'denmark',
    SENSOR_ID = 'bme280_1',
    LOCATION = 'room_1',
    OWNER = 'jsanda',
    QUANTITY_UNITS_ILLUMINANCE = 'lux',
    QUANTITY_UNITS_PRESSURE = 'hPa',
    QUANTITY_UNITS_TEMPERATURE = 'degrees',
    QUANTITY_UNITS_HUMIDITY = 'percent',
    QUANTITY_TYPE_ILLUMINANCE = 'illuminance',
    QUANTITY_TYPE_PRESSURE = 'pressure',
    QUANTITY_TYPE_TEMPERATURE = 'temperature',
    QUANTITY_TYPE_HUMIDITY = 'humidity',
    TOPIC_ILLUMINANCE = 'voicehome/sensors/illuminance',
    TOPIC_PRESSURE = 'voicehome/sensors/pressure',
    TOPIC_TEMPERATURE = 'voicehome/sensors/temperature',
    TOPIC_HUMIDITY = 'voicehome/sensors/humidity',
    TOPIC_SUBSCRIBE_LIGHTS='voicehome/lights/command',
    TOPIC_SUBSCRIBE_LIGHTS_STATE='voicehome/lights/state/command',
    TOPIC_LIGHTS_STATE='voicehome/lights/state/receive',
    TOPIC_MEASURE_COMMAND='voicehome/sensors/command',
    KEEPALIVE = 60,
    PORT = 1883)