### Voicehome Module

#### Add a new module
* Have an idea, design physical devices
* Use the tools
    * MQTT communication
    * Mongo Database
    * Tornado Webserver with websockets
* Control your functionality, user-defined commands
    * Keyboard control
    * Voice control
    
#### Specifications
1. create a new folder in ```voicehome/modules/```, name of this folder is the name of your module (```<module_name>```)
2. create three mandatory files:
    * ```voicehome/modules/<module_name>/metadata.json```
        * example:
        ```
        {
          "module_id": "sensors",
          "description": "Sensory system - temperature, illuminance, pressure, motion",
          "mqtt_topics": ["voicehome/sensors", "voicehome/sensors/temperature"],
          "websocket_passports": ["sensors"],
          "moves": [
            {
              "move_id": "sensors_01.get_current_temperature",
              "method_name": "get_current_temperature",
              "description": "Sends a command via MQTT to measure the current temperature.",
              "calls": [
                ["kolik je stupňů"],
                ["jaká je teplota"],
                ["změř", "teplotu"]
              ]
            }
          ]
        }
        ```
        * ```"module_id" = "<module_name>"```
        * ```"description"``` module description (brief)
        * ```"mqtt_topics"``` MQTT topics this module wants to subscribe
        * ```"websocket_passports"``` websocket message with these "passport" values will be passed to this module
        * ```"moves"``` list of moves (actions), this module is capable of
            * ```move_id``` an unique ID, try to keep the convention: ```<module_name>_<order_in_this_list>.<method_name>```
            * ```method_name``` name of the corresponding Python method in ```<module_name>.py```
            * ```description``` move description (brief)
            * ```calls``` list of calls (commands) firing this move; it's a list of lists of strings (must fit the chosen LOGIC)
    * ```voicehome/modules/<module_name>/<module_name>.py```
        * for every ```move``` in ```metadata.json```, this file must implement a method with the corresponding ```method_name```
        * keep first 6 lines from the following example
        * example:
        ```
        from modules.voicehome_module import VoicehomeModule

        class Sensors(VoicehomeModule):
        
            def __init__(self, engine, dir_path):
                VoicehomeModule.__init__(self, engine, dir_path)
        
            def get_current_temperature(self):
                payload = {'command': 'measure_temperature'}
                self.mqtt_publish(topic='voicehome/sensors/commands', payload=payload)
                print('Module '+self.id+': command to measure temperature sent.')
        
            def on_mqtt_message(self, msg):
                if msg['key'] == 'current_temperature':
                    self.reply(message='Aktuální teplota je: '+str(msg['value']))
        ```
        
    * ```voicehome/modules/<module_name>/README.md```
        * describe your module
3. Run ```$ python voicehome/backend/engine.py```. The module will be automatically loaded. You can then test your commands (e.g. from the Keyboard controller - see ```voicehome/backend/controllers/README.md```) and check it from the GUI (by default automatically passed via JSON handler ```engine.webserver.packet["modules"]```)

#### Tools - specifications

##### MQTT
- broker access info on Google Drive
- topic structure: ```voicehome/<module_name>/<module-specific_category>```
- send data to broker (example):
```
topic = 'voicehome/lights/led'
payload = {'led_color': 'red', 'set_state': 'on'}
self.mqtt_publish(topic, payload)
```
- subscribe from broker
    - in ```<module_name>/metadata.json```, list the topics you want to subscribe (```mqtt_topics```)
    - in ```<module_name>/<module_name>.py```, implement ```def on_mqtt_message(self, msg)```

##### Mongo Database

- save item to the database:
    ```
    item = {
      "key": "voicehome/<module_name>/<module-specific_category>", 
      "payload": {<your_structured_data>}
    }
    self.save_to_mongo(self.id, item)
    ```
    - ```item``` example:
        ```
        {
          "key": "voicehome/sensors/temperature", 
          "payload": {
            "sensor_id": "livingroom_ds18b20",
            "timestamp": "2019-12-02 10:46:30",
            "value": 25.2,
            "status": "ok"
          }
        }
        ```             
- read from the database
    ```
    query = {'key': 'voicehome/<module_name>/<module-specific_category>'}
    res = self.search_mongo(self.id, query)
    ```
    - ```query``` example
    ```
    {'key': 'voicehome/sensors/temperature'}
    ```
    - returns (what we get in ```res```) - list of items fitting the key in query
    ```
        [{"sensor_id": "livingroom_ds18b20",
                   "timestamp": "2019-12-02 10:47:30",
                   "value": 25.2,
                   "status": "ok"},
         {"sensor_id": "livingroom_ds18b20",
                   "timestamp": "2019-12-02 10:48:30",
                   "value": 25.9,
                   "status": "ok"},
         ...]
    ```
  
##### Tornado Webserver with WebSockets
- asynchronous communication with your frontend
- send a message to the frontend:
    ```
    msg = {'passport': '<required_key_of_msg>', ...<your_structure>...}
    self.websocket_send(msg)
    ```
    - example
        ```
        msg = {'passport': 'sensors/temperature',
               'current_value': 24,
               'day_average': 21
        }
        self.websocket_send(msg)
        ```
- catch messages from the frontend
    - in ```<module_name>/metadata.json```, list the passports you want to catch (```websocket_passports```)
    - in ```<module_name>/<module_name>.py```, implement ```def on_websocket_message(self, msg)```
               
#### System methods for modules (so far)

* You implement those (override parent):
    - ```def on_mqtt_message(self, msg)```
        * ```msg: <paho-mqtt msg>```, access ```msg.topic```, ```msg.payload```
        * called each time something is published to one of the topics this module is subscribing (defined in ```metadata.json```)
    
    - ```def on_websocket_message(self, msg)```
        * ```msg: dict```, should include the "passport" key
        * called each time a websocket is sent and includes one of the "passport" values defined in ```metadata.json```)v

* You call those:
    - ```self.reply(message)```
        * ```message: str```
        * module's reply to the controller
    
    - ```self.save_to_mongo(module_id, item)```
        * ```module_id: str```, every module has it on: ```self.id```, equals the <modoule_name>
        * ```item: dict```, structure is module-dependent
        * will save your data to the database
    
    - ```self.search_mongo(module_id, query)```
        * ```module_id: str```, every module has it on: ```self.id```, equals the <modoule_name>
        * ```query: dict```, just one (key, value) pair
        * returns a list of all items from the database having the given (key, value) pair
        
    - ```self.mqtt_publish(topic, payload)```
        * ```topic: str```
        * ```payload: dict or str```
        * publish an MQTT message to the broker
        
    - ```self.websocket_send(msg)```
        * ```msg: dict```, should include the "passport" key
        * send a websocket message (from the server to the GUI)