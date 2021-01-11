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
    SERVER='147.228.124.230',
    USER='sanda',
    PASSWD='denmark',
    SENSOR_ID='room_2',
    LOCATION='room_2',
    OWNER='jsanda',
    QUANTITY_TEMPERATURE='degrees',
    TOPIC_TEMPERATURE='voicehome/sensors/temperature',
    TOPIC_CURRENT_TEMPERATURE_COMMAND='voicehome/sensors',
    TOPIC_SUBSCRIBE_LED='voicehome/lights/led',
    TOPIC_SUBSCRIBE_COMMAND='voicehome/sensors/commands',
    KEEPALIVE=60,
    PORT=1883)
