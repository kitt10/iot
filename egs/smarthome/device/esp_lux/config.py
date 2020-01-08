#CONFIGURATION FILE WITH PARAMETERS

PARAMS = dict(
    ENABLE_EXTERNAL_LED = True,
    ENABLE_INTERNAL_LED = True)

GPIO = dict(
    EXTERNAL_LED = 13,
    TSL_SCL = 5,
    TSL_SDA = 4)    

WIFI = dict(
    SSID = '',
    PASSWD = '')

MQTT = dict(     
    SERVER = '147.228.124.68',
    USER = 'patrik', 
    PASSWD = 'makamnaprj4',
    SENSOR_ID = 'tsl2591_01',
    LOCATION = 'room',
    OWNER = 'pn',
    QUANTITY = 'illuminance',
    ILLUMINANCE_TOPIC = 'smarthome/room/illuminance/',
    KEEPALIVE = 60,
    PORT = 1883)