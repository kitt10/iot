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
    SERVER = '147.228.124.230',
    USER = 'sanda', 
    PASSWD = 'denmark',
    SENSOR_ID = 'tsl2591',
    LOCATION = 'room',
    OWNER = 'pn',
    QUANTITY = 'illuminance',
    TOPIC_SENSOR = 'test_sensor',
    TOPIC_SUBSCRIBE = 'voicehome/lights/led',
    KEEPALIVE = 60,
    PORT = 1883)