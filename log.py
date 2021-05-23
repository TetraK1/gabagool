import serial
import time
import json
import paho.mqtt.publish as mqttpublish

broker='broker.hivemq.com'
broker='broker.emqx.io'
topic='emberbox/curing/data'

ser = serial.Serial('/dev/ttyUSB0')
ser.flushInput()

while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes.decode("utf-8").strip()

        try:
            data = json.loads(decoded_bytes)
        except:
            print('Bad data:', decoded_bytes)
            continue

        msg = {"time":time.time(), "data":data}
        print(msg['data'])

        try:
            mqttpublish.single(topic=topic, payload=json.dumps(msg), hostname=broker)
        except:
            print("Publishing to mqtt failed.")

        with open("log.txt","a") as f:
            f.write(json.dumps(msg) + '\n')
    except Exception as e:
        print(e)
        print("Keyboard Interrupt")
        break
