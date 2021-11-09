### The Engine
---
- MQTT Subscriber 
- Webserver
- Neural network based decision system
---
#### cfg_engine.yml
```yaml
broker:
  host:                     # string
  port:                     # number
  uname:                    # string
  passwd:                   # string
  topic: 'smartblinds/#'    # string
  verbose: false            # boolean
mongo:
  host:                     # string
  port:                     # number
  database: 'smartblinds'   # string
  collection: 'real'        # string [real / sim]
  verbose: true             # boolean
verbose: true               # boolean
```
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