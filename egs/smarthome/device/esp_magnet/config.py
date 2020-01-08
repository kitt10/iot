#CONFIGURATION FILE WITH PARAMETERS

PARAMS = dict(
    ENABLE_EXTERNAL_LED_1 = True,
    ENABLE_EXTERNAL_LED_2 = True,
    ENABLE_INTERNAL_LED = True)

GPIO = dict(
    EXTERNAL_LED_1 = 0,
    EXTERNAL_LED_2 = 5,
    MAGNET_1 = 12,
    MAGNET_2 = 13)    

WIFI = dict(
    SSID = '',
    PASSWD = '')

MQTT = dict(     
    SERVER = '147.228.124.68',
    USER = 'patrik', 
    PASSWD = 'makamnaprj4',
    SENSOR_1_ID = 'ls311b38_01',
    SENSOR_2_ID = 'ls311b38_02',
    LOCATION = 'room',
    OWNER = 'pn', 
    QUANTITY_1 = 'door_open',
    QUANTITY_2 = 'window_open',
    TOPIC_1 = 'smarthome/room/door_open',
    TOPIC_2 = 'smarthome/room/window_open',
    KEEPALIVE = 60,
    PORT = 1883)