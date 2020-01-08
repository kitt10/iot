#CONFIGURATION FILE WITH PARAMETERS

PARAMS = dict(
    ENABLE_EXTERNAL_LED = True,
    ENABLE_INTERNAL_LED = True)

GPIO = dict(
    EXTERNAL_LED = 13,
    DS18B20_INSIDE = 5,
    DS18B20_OUTSIDE = 14,
    DHT11 = 0)    

WIFI = dict(
    SSID = '',
    PASSWD = '')

MQTT = dict(     
    SERVER = '147.228.124.68',
    USER = 'patrik', 
    PASSWD = 'makamnaprj4',
    SENSOR_1_ID = 'ds18b20_01',
    SENSOR_2_ID = 'ds18b20_02',
    SENSOR_3_ID = 'dht11_01',
    OWNER = 'pn',
    QUANTITY_1 = 'temperature',
    QUANTITY_2 = 'humidity',
    LOCATION_1 = 'room',
    LOCATION_2 = 'outside',
    TEMPERATURE_IN_TOPIC = 'smarthome/room/temperature',
    TEMPERATURE_OUT_TOPIC = 'smarthome/outside/temperature',
    HUMIDITY_TOPIC = 'smarthome/room/humidity',
    KEEPALIVE = 60,
    PORT = 1883)