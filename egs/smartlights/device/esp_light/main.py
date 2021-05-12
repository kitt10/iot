from umqtt.simple import MQTTClient
from machine import Pin
import ubinascii
import machine
import ujson as json
import config as cfg
import gc
import time
import ntptime

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
pins = {}
states = {}
for led in cfg.LEDS:
    pins[led] = Pin(cfg.LEDS[led], Pin.OUT)
    pins[led].off()
    states[led] = 0

def callback(topic, msg):
    try:
        msg_d = json.loads(msg)
        if(msg_d.get("cmd") == "change_status"):
            p = pins.get(msg_d.get("LED"), False)
            if(p):
                if(msg_d.get("status") == 1):
                    p.on()
                    states[msg_d.get("LED")] = 1
                    msg_s = dict(leds = [msg_d.get("LED")], states = [1])
                elif(msg_d.get("status") == 0):
                    p.off()
                    states[msg_d.get("LED")] = 0
                    msg_s = dict(leds = [msg_d.get("LED")], states = [0])
                else:
                    msg_s = {"error": {"code": 1, "description": "Invalid status, use 0 or 1."}}
            else:
                msg_s = {"error": {"code": 2, "description": "This LED wasn't found."}}
        elif(msg_d.get("cmd") == "get_status"):
            msg_s = {"leds": list(cfg.LEDS), "states": list(states.values())}
        else:
            msg_s = {"error": {"code": 3, "description": "Unknown command."}}
    except:
        msg_s = {"error": {"code": 4, "description": "Unexpected error, check payload."}}
    finally:
        msg = json.dumps(msg_s)
        client.publish(cfg.MQTT["STATUS_TOPIC"], msg)

ntptime.settime()

client = MQTTClient(CLIENT_ID, cfg.MQTT["BROKER"], cfg.MQTT["PORT"], cfg.MQTT["USER"], cfg.MQTT["PASSWD"])
client.set_callback(callback)
client.connect()
client.subscribe(cfg.MQTT["COMMAND_TOPIC"])

try:
    while 1:
        client.wait_msg()
finally:
    client.disconnect()