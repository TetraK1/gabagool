import datetime as dt
import matplotlib.pyplot as plt
import json
import time
import requests

def main():
    r = requests.get('https://emberbox.net/curing/api/readings/?last=86400')
    if r.status_code != 200:
        print('Getting data failed with status code', r.status_code)

    data = r.json()
    data = data[::60]
    for dp in data: dp['time'] = dt.datetime.fromtimestamp(dp['time'])
    data = [dp for dp in data if dp['time'] > dt.datetime.now() - dt.timedelta(days=1)]

    time = [dp['time'] for dp in data]

    plt.style.use('ggplot')

    plot_temp(time, [dp['temperature'] for dp in data])
    plot_humidity(time, [dp['humidity'] for dp in data])
    plot_pressure(time, [dp['pressure'] for dp in data])
    plot_altitude(time, [dp['altitude'] for dp in data])
    plt.close('all')

def plot_temp(time, temp):
    f, ax = plt.subplots()
    ax.plot(time, temp)
    ax.title.set_text("Temperature")
    ax.set_ylabel('°C')
    f.autofmt_xdate()
    f.savefig('plots/temp.png')

def plot_humidity(time, humidity):
    f, ax = plt.subplots()
    ax.plot(time, humidity)
    ax.title.set_text("Humidity")
    ax.set_ylabel('RH%')
    f.autofmt_xdate()
    f.savefig('plots/humidity.png')

def plot_pressure(time, pressure):
    f, ax = plt.subplots()
    ax.plot(time, pressure)
    ax.title.set_text("Barometric Pressure")
    ax.set_ylabel('Pa')
    f.autofmt_xdate()
    f.savefig('plots/pressure.png')

def plot_altitude(time, altitude):
    f, ax = plt.subplots()
    ax.plot(time, altitude)
    ax.title.set_text("Virtual Altitude")
    ax.set_ylabel('m')
    f.autofmt_xdate()
    f.savefig('plots/altitude.png')

if __name__ == '__main__':
    main()
