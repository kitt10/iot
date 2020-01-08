# MQTT topic

General structure
```
{project}/{location}/{quantity}
```

Example
```
smarthome/livingroom/temperature
```

# MQTT message

Interface
```
{
    "sensor_id": string
    "timestamp": string
    "value": float
    "status": string
    "quantity": string
    "location": string
    "owner": string    
}
```

Example
```json
{
    "sensor_id": "dht11_01",
    "timestamp": "2019-12-02 10:46:30",
    "value": 25.2,
    "status": "ok",
    "quantity": "temperature",
    "location": "livingroom",
    "owner": "pn"   
}
```

# Project smarthome

## Project name

```
{project} = "smarthome"
```

## List of owners

```
pn
```

## List of locations

```
room
outside
```

## List of quantities

```
temperature
humidity
illuminance
pressure
motion
door_open
window_open
```

## List of topics

```
smarthome/outside/temperature
smarthome/room/temperature
smarthome/room/humidity
smarthome/room/illuminance
smarthome/room/pressure
smarthome/room/motion
smarthome/room/door_open
smarthome/room/window_open
```

## List of sensors

```
bme280_01
dht11_01
ds18b20_01
ds18b20_02
ls311b38_01
ls311b38_02
tsl2591_01
am312_01
```

## List of ESPs

```
esp_lux
esp_magnet
esp_pir
esp_pressure
esp_temphumid
```

## Specifications

### ESP ```esp_lux```
```
location: "room"
owner: "pn"
timestamp: "XXX"
status: {"ok", "sensor_error"}
```
#### sensor ```tsl2591_01```

```
sensor_id: "tsl2591_01"
```

topic: ```smarthome/room/illuminance```

```
value: <0, lux_max>
quantity: "illuminance"
```

### ESP ```esp_magnet```
```
location: "room"
owner: "pn"
timestamp: "XXX"
status: {"ok", "sensor_error"}
```
#### sensor ```ls311b38_01```

```
sensor_id: "ls311b38_02"
```

topic: ```smarthome/room/door_open```

```
value: {0, 1}
quantity: "door_open"
```

#### sensor ```ls311b38_02```

```
sensor_id: "ls311b38_01"
```

topic: ```smarthome/room/window_open```

```
value: {0, 1}
quantity: "window_open"
```

### ESP ```esp_pir```
```
location: "room"
owner: "pn"
timestamp: "XXX"
status: {"ok", "sensor_error"}
```
#### sensor ```am312_01```

```
sensor_id: "am312_01"
```

topic: ```smarthome/room/motion```

```
value: {1}
quantity: "motion"
```

### ESP ```esp_pressure```
```
location: "room"
owner: "pn"
timestamp: "XXX"
status: {"ok", "sensor_error"}
```
#### sensor ```bme280_01```

```
sensor_id: "bme280_01"
```

topic: ```smarthome/room/pressure```

```
value: <0, pressure_max>
quantity: "pressure"
```

topic: ```smarthome/room/temperature```

```
value: <t_min, t_max>
quantity: "temperature"
```

### ESP ```esp_temphumid```
```
owner: "pn"
timestamp: "XXX"
status: {"ok", "sensor_error"}
```
#### sensor ```ds18b20_01```

```
location: "room"
sensor_id: "ds18b20_01"
```

topic: ```smarthome/room/temperature```

```
value: <t_min, t_max>
quantity: "temperature"
```

#### sensor ```ds18b20_02```

```
location: "outside"
sensor_id: "ds18b20_02"
```

topic: ```smarthome/outside/temperature```

```
value: <t_min, t_max>
quantity: "temperature"
```

#### sensor ```dht11_01```

```
location: "room"
sensor_id: "dht11_01"
```

topic: ```smarthome/room/temperature```

```
value: <t_min, t_max>
quantity: "temperature"
```

topic: ```smarthome/room/humidity```

```
value: <0, 100>
quantity: "humidity"
```