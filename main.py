import asyncio
import network
import time

# https://microdot.readthedocs.io/en/latest/index.html
from microdot import Microdot, Response

from lights import PwmLight
from settings import Settings

wifi_settings = Settings("wifi")
wlan = network.WLAN(network.STA_IF)
app = Microdot()

light_settings = Settings("light", {"on": False, "brightness": 100})
light = PwmLight(4, light_settings.get("on"), light_settings.get("brightness"))

async def connectionTask():
    
    ssid = wifi_settings.get("ssid")
    password = wifi_settings.get("pass")
    while True:
        if not wlan.isconnected():
            wlan.active(True)
            wlan.config(pm=0xA11140)
            wlan.connect(ssid, password)
            for i in range(0,100):
                print(f"#{i} Connecting to {ssid} ({wlan.status()})")
                if wlan.isconnected():
                    print(f"Connected to {ssid} - {wlan.ifconfig()[0]}")
                    break
                time.sleep(.5)
        time.sleep(1)

@app.get("/")
async def state_handler(_):
    state = light.get_state()
    return Response(body=state)

@app.put("/")
async def update_handler(request):
    data = request.json
    if "on" in data:
        if data["on"]:
            light.turn_on()
        else:
            light.turn_off()
    if "brightness" in data:
        light.set_brightness(data["brightness"])
    light_settings.save_settings(light.get_state())


asyncio.run(app.start_server(port=80, debug=True))
asyncio.run(connectionTask())
