#!flask/bin/python

"""
aiCar gate Control
created for RPi

by Adam Yusenko

ver. by 07.12.2022
"""
import os
import sys
from subprocess import check_call
import pip
import time
import configparser


def install(package):
    try:
        pip.main(['install', package])
    except AttributeError:
        check_call([sys.executable, '-m', 'pip', 'install', package])
    os.execl(sys.executable, sys.executable, *sys.argv)


try:
    from flask import Flask, jsonify, abort
except ModuleNotFoundError:
    print("Flask is not installed."
          + "Try to automatically install it"
          + "If it fails, please manually execute"
          + "python3 -m pip install flask")
    install("flask")

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print("rpi.gpio is not installed."
          + "Try to automatically install it"
          + "If it fails, please manually execute"
          + "python3 -m pip install RPi.GPIO")
    install("RPi.GPIO")

app = Flask(__name__)
config = configparser.RawConfigParser()

try:
    config.read('./config.ini')
    RELAY_ON_PIN = config.getint('Relay', 'relay_on')
    RELAY_OFF_PIN = config.getint('Relay', 'relay_off')
    DELAY_ON = config.getint('Relay', 'delay_on')
    DELAY_OFF = config.getint('Relay', 'delay_off')

    PORT = config.getint('Flask', 'port')
    HOST = config.get('Flask', 'host')
    DEBUG = config.getboolean('Flask', 'debug')
    METHODS = config.get('Flask', 'methods')
except FileNotFoundError:
    app.logger.critical(f"Config file is not found ")

# #  set mode for rpi gpio
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup relay for open gate
GPIO.setup(RELAY_ON_PIN, GPIO.OUT)
GPIO.output(RELAY_ON_PIN, GPIO.LOW)

# Setup relay for close  gate
GPIO.setup(RELAY_OFF_PIN, GPIO.OUT)
GPIO.output(RELAY_OFF_PIN, GPIO.LOW)

# returns for flask server
tasks = [
    {
        'id': 1,
        'title': u'Open gate',
        'description': u'Open gate on command ',
        'done': True
    },
    {
        'id': 2,
        'title': u'Close gate',
        'description': u'Close gate on command',
        'done': True
    }
]


# open relay
def relay_ON():
    GPIO.output(RELAY_ON_PIN, GPIO.HIGH)
    time.sleep(DELAY_ON)
    GPIO.output(RELAY_ON_PIN, GPIO.LOW)
    return jsonify(tasks[0])


# close relay
def relay_OFF():
    GPIO.output(RELAY_OFF_PIN, GPIO.HIGH)
    time.sleep(DELAY_OFF)
    GPIO.output(RELAY_OFF_PIN, GPIO.LOW)
    return jsonify(tasks[1])


@app.route('/relay/<string:relay_data>', methods=[METHODS])
def relay_one(relay_data):
    return_data = ''
    if relay_data == 'on':
        return_data = relay_ON()
    elif relay_data == 'off':
        return_data = relay_OFF()
    else:
        abort(404)
    return return_data


if __name__ == '__main__':
    app.run(host=HOST, debug=DEBUG, port=PORT)
