### Topics:
Commands: `smartlights/ESP0/cmd`
Status: `smartlights/ESP0/status`

Commands topic is used to send commands to an ESP8266 which replies with status messages in the Status topic.

### Commands:
There are two different commands available:
1. Turn a LED called `LED_name` on/off:

    - on:

        ```JSON
        {
            "cmd": "change_status",
            "LED": "LED_name",
            "status": 1
        }
        ```
        Possible to use a Mosquitto command `mosquitto_pub -d -u vbrenik -P makamnaprj -t smartlights/ESP0/cmd -m "{\"LED\": \"BILA\", \"cmd\": \"change_status\", \"status\":0}"`

    - off:

        ```JSON
        {
            "cmd": "change_status",
            "LED": "LED_name",
            "status": 0
        }
        ```
        Possible to use a Mosquitto command `mosquitto_pub -d -u vbrenik -P makamnaprj -t smartlights/ESP0/cmd -m "{\"LED\": \"BILA\", \"cmd\": \"change_status\", \"status\":1}"`

2. Get a list of configured LEDs and their current state:

    ```JSON
    {
        "cmd": "get_status"
    }
    ```

Reply on the Status topic is always in this format:

```JSON
{
    "leds": ["LED_1", "LED_2"], 
    "states": [0, 1]
}
```

On `get_status` command all LEDs and their states are returned. On `change_status` command only affected LEDs are returned.