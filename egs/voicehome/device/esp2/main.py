#!/usr/bin/env python
# coding: utf-8
import time
import gc
from mqttclient import Client
import config

# initialization
mqtt_client = Client()

msg_structure_state = {'ID': config.MQTT['LightsID'][0],
                       'type': 'light',
                       'state': mqtt_client.light1.value()
                       }
print(msg_structure_state)
mqtt_client.mqtt_msg(msg_structure_state,
              config.MQTT['TOPIC_LIGHTS_STATE'])

# mqtt_client_commands = Client()
gc.disable()
# gc.enable()
gc.collect()
mqtt_client.connect()


# main loop
while True:
    time.sleep(2)
    # print(gc.mem_free())
    if gc.mem_free() < 10000:
        gc.collect()
    # try:
    # print(mqtt_client.sync_time())
    # subscribe selected topic
    mqtt_client.subscribe()
    # publish value every minute
    if(mqtt_client.last_minute_sent != mqtt_client.get_min() and mqtt_client.get_sec() in range(20, 23)):

        mqtt_client.publish()
        # mqtt_client.measure_temperature_now = False
    # except:
    #     mqtt_client.client.disconnect()
