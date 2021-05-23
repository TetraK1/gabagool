import paho.mqtt.client as mqtt
import json

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("emberbox/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
    except Exception as e:
        print("Bad data:", msg.payload)
        print(e)
        return

    with open('log.txt', 'a') as f:
        f.write(json.dumps(data) + '\n')
        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.emqx.io", 1883, 60)
client.loop_forever()