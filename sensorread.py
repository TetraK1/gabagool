import serial
import time
import json
import paho.mqtt.publish as mqttpublish
import requests

broker='broker.hivemq.com'
broker='broker.emqx.io'
topic='emberbox/curing/data'

ser = serial.Serial('/dev/ttyUSB0')
ser2 = serial.Serial('/dev/ttyUSB1')
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

        try:
            data2 = {i: msg['data'][i] for i in msg['data']}
            data2['time'] = msg['time']
            result = requests.post('https://emberbox.net/curing/api/readings/', json=data2)
            status = result.status_code
            if status != 200: print(f'Post error code {status}')
        except KeyboardInterrupt: raise
        except Exception as e:
            print("Posting data failed.")
            print(e)

        if msg['data']['temperature'] > 12.5:
            ser2.write('1'.encode('utf-8'))
        elif msg['data']['temperature'] < 11.5:
            ser2.write('0'.encode('utf-8'))

        with open("log.txt","a") as f:
            f.write(json.dumps(msg) + '\n')
    except Exception as e:
        print(e)
        print("Keyboard Interrupt")
        break
