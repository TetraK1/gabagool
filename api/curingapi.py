import flask
from flask import request
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

with sqlite3.connect('fridge.db') as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS "bme280_data" (
        "time"	INTEGER NOT NULL,
        "temperature"	REAL,
        "humidity"	REAL,
        "pressure"	REAL,
        "altitude"	REAL,
        PRIMARY KEY("time")
    );''')
    conn.commit()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/readings/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return post_data()
    conn = sqlite3.connect('fridge.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    params = flask.request.args
    after = request.args.get('after', 0)
    limit = request.args.get('last', 100)
    return flask.jsonify(cur.execute('SELECT * FROM bme280_data WHERE time > ? ORDER BY time DESC LIMIT (?)', (after,limit)).fetchall())

def post_data():
    data = request.json
    with sqlite3.connect('fridge.db') as conn:
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO bme280_data(time, temperature, humidity, pressure, altitude) VALUES(?,?,?,?,?)',
            (data['time'], data['temperature'], data['humidity'], data['pressure'], data['altitude'])
        )
        conn.commit()

    return ''

if __name__ == '__main__':
    app.run()