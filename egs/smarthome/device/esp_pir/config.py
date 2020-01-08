#CONFIGURATION FILE WITH PARAMETERS

PARAMS = dict(
    ENABLE_EXTERNAL_LED = True,
    ENABLE_INTERNAL_LED = True,
    ENABLE_BUZZER = False)

GPIO = dict(
    EXTERNAL_LED = 13,
    BUZZER = 5,
    PIR = 14)    

WIFI = dict(
    SSID = '',
    PASSWD = '')

MQTT = dict(     
    SERVER = '147.228.124.68',
    USER = 'patrik', 
    PASSWD = 'makamnaprj4',
    SENSOR_ID = 'am312_01',
    LOCATION = 'room',
    OWNER = 'pn',
    QUANTITY = 'motion',
    MOTION_TOPIC = 'smarthome/room/motion',
    KEEPALIVE = 60,
    PORT = 1883)