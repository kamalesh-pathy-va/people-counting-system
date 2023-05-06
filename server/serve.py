from flask import Flask, jsonify, render_template, url_for
import pickle

import os

app = Flask(__name__)

@app.route('/inout')
def inout():
    with open('/home/kamaleshpathy/Downloads/final_test/value.pkl', 'rb') as f:
        value = pickle.load(f)
    value = value.split(',')
    data = {'in': value[0], 'out': value[1]}
    return jsonify(data)

@app.route('/temp')
def temp():
    temp = os.popen('cat /sys/class/thermal/thermal_zone0/temp')
    temp = temp.readlines()[0][:-1]
    temp = str(int(temp)/1000)
    return temp

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2610)
