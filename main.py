# https://microdot.readthedocs.io/en/latest/index.html

from microdot import Microdot
from microdot import send_file

import network
import time

from lights import PwmLight
from settings import Settings

from machine import Pin

onboard_led = Pin('LED', Pin.OUT)
light = PwmLight(4)
settings = Settings('wifi.dat').get_settings()

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
        
app = Microdot()



@app.route('/')
def hello(request):
    return send_file('/html/index.html')

@app.get('/on')
def turn_on_handler(request):
    light.turn_on()
    return 'Turning on', 200, {'Content-Type': 'text/html'}

@app.get('/off')
def turn_off_handler(request):
    light.turn_off()
    return 'Turning off', 200, {'Content-Type': 'text/html'}

@app.get('/status')
def get_status(req):
    return str(1 if light.is_on else 0)

@app.get('/brightness_value')
def get_brightness(req):
    return str(light.brightness)

"""
"brightness_url": "http://192.168.1.206/light/brightness?value=2"
"""
@app.get('/brightness')
def set_brightness(req):
    brightness = int(req.args.get('value'))
    light.set_brightness(brightness)
    

print("Connecting to network")
connect_to_network(settings['ssid'], settings['pass'])

app.run(debug=True)