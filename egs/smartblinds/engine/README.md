### The Engine
---
- MQTT Subscriber 
- Webserver
- Neural network based decision system
---
#### broker2mongo.py
- running separately
- MQTT broker subscriber
- saving data to MongoDB

##### MQTT
- topics
```
smartblinds/lux/out
smartblinds/lux/Vojta
smartblinds/temp/out
smartblinds/temp/Vojta
```
- expected message structure
```
{
    quantity: string
    value: number
    time: {
        year_day: number
        week_day: number
        day_seconds: number
    }
}
```
##### Database
- database: ```'smartblinds'```
- collections: ```['real', 'sim']```
- DB item structure
```
{
    _id: ObjectId
    timestamp: string
    location: string
    quantity: string
    value: number
    time: {
        year_day: number
        week_day: number
        day_seconds: number
    }
}
```