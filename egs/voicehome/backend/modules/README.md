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

#### Available methods for modules (so far)

- ```def on_mqtt_message(self, msg)```
    * ```msg: <paho-mqtt msg>```, access ```msg.topic```, ```msg.payload```
    * called each time something is published to one of the topics this module is subscribing (defined in ```metadata.json```)

- ```def on_websocket_message(self, msg)```
    * ```msg: dict```, should include the "passport" key
    * called each time a websocket is sent and includes one of the "passport" values defined in ```metadata.json```)v

- ```def reply(self, message)```
    * ```message: str```
    * module's reply to the controller

- ```def save_to_mongo(self, module_id, payload)```
    * ```module_id: str```, every module has it on: ```self.id```, equals the <modoule_name>
    * ```payload: dict```, structure is module-dependent
    * will save your data to the database

- ```def search_mongo(self, module_id, query)```
    * ```module_id: str```, every module has it on: ```self.id```, equals the <modoule_name>
    * ```query: dict```, just one (key, value) pair
    * returns a list of all items from the database having the given (key, value) pair
    
- ```def mqtt_publish(self, topic, payload)```
    * ```topic: str```
    * ```payload: dict or str```
    * publish an MQTT message to the broker
    
- ```def websocket_send(self, msg)```
    * ```msg: dict```, should include the "passport" key
    * send a websocket message (from the server to the GUI)