
##### MQTT
- topics
```
smartblinds/lux/out
smartblinds/lux/Vojta
smartblinds/temp/out
smartblinds/temp/Vojta
smartblinds/temp/max
smartblinds/temp/forecast/1h
smartblinds/temp/forecast/2h
smartblinds/temp/forecast/3h
smartblinds/tilt/Vojta
smartblinds/position/Vojta
smartblinds/owm_code
smartblinds/wind/speed
smartblinds/wind/heading
```
- expected message structure (illuminance, temperature, wind speed and heading, weather code)
```json
{
    quantity: string
    id: string                   //identifier of the feature
    value: number
    time: {
        year_day: number
        week_day: number
        day_seconds: number
    }
}
```
or (blinds tilt and position)
```json
{
    quantity: string
    value: number
    home: boolean               //true if user is at home
    time: {
        year_day: number
        week_day: number
        day_seconds: number
    }
}
```
There are 7 quantities measured or obtained from APIs: ```illuminance``` [lux] and ```temperature``` [°C] (outside - ```out```, inside - ```Vojta```, maximum day temperature - ```max```, forecast temperature - ```forecast/xh```, where ```x``` is 1 to 3 hours in to the future), both ```position``` <0, 100> and ```tilt``` <0, 100> of blinds, ```wind_speed``` [m/s], ```wind_heading``` [°] and OpenWeatherMap weather code - ```owm_code```.
##### Database
- database: ```'smartblinds'```
- collections: ```['real', 'sim']```
- DB item structure
```
{
    _id: ObjectId
    timestamp: string
    data: {
      location: string
      quantity: string
      value: number
      time: {
          year_day: number
          week_day: number
          day_seconds: number
      }
    }
}
```