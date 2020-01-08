#CONFIGURATION FILE WITH PARAMETERS

PARAMS = dict(
    ENABLE_EXTERNAL_LED = True,
    ENABLE_INTERNAL_LED = True)

GPIO = dict(
    EXTERNAL_LED = 5,
    BME_SCL = 14,
    BME_SDA = 12)    

WIFI = dict(
    SSID = '',
    PASSWD = '')

MQTT = dict(     
    SERVER = '147.228.124.68',
    USER = 'patrik', 
    PASSWD = 'makamnaprj4',
    SENSOR_ID = 'bme280_01',
    LOCATION = 'room',
    OWNER = 'pn',
    QUANTITY_1 = 'pressure',
    QUANTITY_2 = 'temperature',
    PRESSURE_TOPIC = 'smarthome/room/pressure',
    TEMPERATURE_TOPIC = 'smarthome/room/temperature',
    KEEPALIVE = 60,
    PORT = 1883)