### Web GUI

- available from: ```147.228.124.230:8881```
- index file: ```index.html```
- static root path: ```voicehome/frontend```
- backend webserver: ```voicehome/backend/webserver.py``` (Python Tornado)

##### Communication backend-frontend

* websockets
    * ```HOST:PORT/websocket```
    * message structure (must have the ```passport``` key):
    ```
    msg = {
        "passport": "<passport_value>"
        ...
    }
    ```
* JSON handler
    * ```HOST:PORT/packet```
    * variable (dict) 
    ```
    engine.webserver.packet = {"modules": [], ...}
    ```

    