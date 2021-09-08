# This script is based on code from several internet sources:
# http://www.steves-internet-guide.com/into-mqtt-python-client/
# https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
# all modifications by F. Ostermann;
# it subscribes to the MQTT topic defined in the publishing script
# NOT intended for production, only demonstration;


import random
from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt/tinyml/"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

client = connect_mqtt()
subscribe(client)
client.loop_forever()