import paho.mqtt.client as mqtt
from json import dumps as dumps_json

BROKER_IP = '147.228.10.10'
BROKER_PORT = 1883
BROKER_UNAME = 'kitt'
BROKER_PASSWD = 's$ecret'
TOPIC = 'smarthome/#'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, mid, qos):
    print('Connected with result code qos:', str(qos))

# The callback for when a PUBLISH message is received from the server.
def on_publish(client, userdata, mid):
    print('On publish mid: ', str(mid))

def send2broker(client, topic, payload, qos=0, retain=False):
    client.publish(topic, payload, qos=qos, retain=False)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.username_pw_set(BROKER_UNAME, password=BROKER_PASSWD)
    client.connect(BROKER_IP, BROKER_PORT, 60)

    send2broker(client, TOPIC, 'Hi, there! [string]')

    send2broker(client, TOPIC, dumps({'message': 'Hi, there! [json]'}), retain=True)

    client.disconnect()
