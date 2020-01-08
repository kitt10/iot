import paho.mqtt.client as mqtt

BROKER_IP = '147.228.10.10'
BROKER_PORT = 1883
BROKER_UNAME = 'kitt'
BROKER_PASSWD = 's$ecret'
TOPIC = 'smarthome/#'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, mid, qos):
    print('Connected with result code qos:', str(qos))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TOPIC)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if (msg.payload == 'Q'):
        client.disconnect()
    
    print(msg.topic, msg.qos, msg.payload)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(BROKER_UNAME, password=BROKER_PASSWD)
    client.connect(BROKER_IP, BROKER_PORT, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and
    # a manual interface.
    client.loop_forever()