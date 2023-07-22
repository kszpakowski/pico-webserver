# https://microdot.readthedocs.io/en/latest/index.html

from microdot import Microdot
from microdot import send_file

import network
import socket
import time

import request_handler as rh
import http_req_parser as rp
from lights import PwmLight
from settings import Settings


from machine import Pin
import uasyncio as asyncio

debug = True

onboard_led = Pin('LED', Pin.OUT)
light = PwmLight(4)
settings = Settings('wifi.dat').get_settings()

state = 'off'
brightness = 100

def connect_to_network(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140)
        
    wlan.connect(ssid,password)

    max_wait = 30
    for _ in range(0,max_wait):
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        print('waiting for connection...')
        onboard_led.toggle()
        time.sleep(0.3)

    if wlan.status() != 3:
        led.value(1)
        raise RuntimeError('network connection failed, error code: ' + str(wlan.status()))
    else:
        status = wlan.ifconfig()
        print('connected, ip = ' + status[0])
        onboard_led.value(0)
        
        
def turn_on():
    global state
    state = 'on'
    onboard_led.value(1)


def turn_off():
    global state
    state = 'off'
    onboard_led.value(0)


app = Microdot()



@app.route('/')
def hello(request):
    #return htmldoc, 200, {'Content-Type': 'text/html'}
    return send_file('/html/index.html')


@app.route('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


@app.get('/on')
def turn_on_handler(request):
    turn_on()
    return 'Turning on', 200, {'Content-Type': 'text/html'}

@app.get('/off')
def turn_off_handler(request):
    turn_off()
    return 'Turning off', 200, {'Content-Type': 'text/html'}

@app.get('/status')
def get_status(req):
    return {
        "state":state,
        "brightness": brightness
        }

print("Connecting to network")
connect_to_network(settings['ssid'], settings['pass'])

app.run(debug=True)