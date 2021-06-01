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

def post_data(data):
    try:
        result = requests.post('https://emberbox.net/curing/api/readings/', json=data, timeout=1)
        status = result.status_code
        if status != 200: print(f'Post error code {status}')
    except Exception as e:
        print("Posting data failed.")
        print(e)

while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes.decode("utf-8").strip()

        try:
            data = json.loads(decoded_bytes)
        except:
            print('Bad data:', decoded_bytes)
            continue

        data['time'] = time.time()
        print(data)

        if data['temperature'] > 13:
            ser2.write(0b10000000.to_bytes(1, 'big'))
        elif data['temperature'] < 12:
            ser2.write(0b00000000.to_bytes(1, 'big'))

        if data['humidity'] < 80:
            ser2.write(0b10000001.to_bytes(1, 'big'))
        elif data['humidity'] > 85:
            ser2.write(0b00000001.to_bytes(1, 'big'))

        threading.Thread(target=post_data, args=(data,)).start()

    except Exception as e:
        print(e)
        print("Keyboard Interrupt")
        break
