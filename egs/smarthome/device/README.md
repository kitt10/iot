## Codes for ESP8266

### LUX SENSOR

- measures illumination [lux]
- esp ID: ```esp_lux```
- list of sensors: ```tsl2591_01```
- sends data to topic: ```smarthome/room/illuminance```

### MAGNET SENSOR

- catches door & window status
- esp ID: ```esp_magnet```
- list of sensors: ```ls311b38_01```, ```ls311b38_02```
- sends data to topic: ```smarthome/room/door_open```, ```smarthome/room/window_open```

### PIR SENSOR

- catches motion in a room 
- esp ID: ```esp_pir```
- list of sensors: ```am312_01```
- sends data to topic: ```smarthome/room/motion```

### PRESSURE SENSOR

- measures barometric pressure & inside temperature
- esp ID: ```esp_pressure```
- list of sensors: ```bme280_01```
- sends data to topic: ```smarthome/room/pressure```, ```smarthome/room/temperature```

### TEMPHUMID SENSOR

- measures temperature inside, temperature outside & humidity inside 
- esp ID: ```esp_temphumid```
- list of sensors: ```ds18b20_01```, ```ds18b20_02```, ```dht11_01```
- sends data to topic: ```smarthome/room/temperature```, ```smarthome/outside/temperature```, ```smarthome/room/humidity```