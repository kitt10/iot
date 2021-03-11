# CONFIGURATION FILE WITH PARAMETERS

PARAMS = dict(
    ENABLE_EXTERNAL_LED=True,
    ENABLE_INTERNAL_LED=True)

GPIO = dict(
    EXTERNAL_LED=13,
    TSL_SCL=5,
    TSL_SDA=4)

WIFI = dict(
    SSID='HP Deskjet 2720 All-in-One',
    PASSWD='PodlahajehnedaStropjebily730')

MQTT = dict(
    ESP_ID=2,
    LightsID=[1],
    SERVER='147.228.124.230',
    USER='sanda',
    PASSWD='denmark',
    SENSOR_ID='ds18b20_1',
    LOCATION='room_2',
    OWNER='jsanda',
    QUANTITY_UNITS_TEMPERATURE = 'degree',
    QUANTITY_TYPE_TEMPERATURE = 'temperature',
    TOPIC_TEMPERATURE='voicehome/sensors/temperature',
    # TOPIC_MEASURE_COMMAND='voicehome/sensors',
    TOPIC_SUBSCRIBE_LIGHTS='voicehome/lights/command',
    TOPIC_SUBSCRIBE_LIGHTS_STATE='voicehome/lights/state/command',
    TOPIC_LIGHTS_STATE='voicehome/lights/state/receive',
    TOPIC_MEASURE_COMMAND='voicehome/sensors/command',
    KEEPALIVE=60,
    PORT=1883)
