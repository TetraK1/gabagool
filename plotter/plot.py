import datetime as dt
import matplotlib.pyplot as plt
import json
import time
import requests
import atmos

def main():
    after = (dt.datetime.now() - dt.timedelta(days=1)).timestamp()
    r = requests.get(f'https://emberbox.net/curing/api/readings/?last=86400&after={after}')
    if r.status_code != 200:
        print('Getting data failed with status code', r.status_code)

    data = r.json()
    data = data[::60]
    for dp in data: dp['time'] = dt.datetime.fromtimestamp(dp['time'])

    time = [dp['time'] for dp in data]

    plt.style.use('ggplot')

    temperature = [dp['temperature'] for dp in data]
    humidity = [dp['humidity'] for dp in data]

    plot_temp(time, temperature)
    plot_humidity(time, humidity)
    plot_pressure(time, [dp['pressure'] for dp in data])
    plot_altitude(time, [dp['altitude'] for dp in data])
    plot_abs_humidity(time, temperature, humidity)
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

def plot_abs_humidity(time, temperature, humidity):
    abs_humidity = [atmos.calculate('AH', T=d[0] + 273.15, RH=d[1], p=1e5) for d in zip(temperature, humidity)]

    f, ax = plt.subplots()
    ax.plot(time, abs_humidity)
    ax.title.set_text("Absolute Humidity")
    ax.set_ylabel('kg/m^3')
    f.autofmt_xdate()
    f.savefig('plots/abs_humidity.png')

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
    while True:
        print("Updating plots...")
        main()
        print("Done")
        time.sleep(60)
