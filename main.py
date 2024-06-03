import asyncio
import network
import time

# https://microdot.readthedocs.io/en/latest/index.html
from microdot import Microdot, Response

from lights import PwmLight
from settings import Settings

from machine import Pin

onboard_led = Pin("LED", Pin.OUT)
wifi_settings = Settings("wifi")

light_settings = Settings("light", {"on": False, "brightness": 100})
light = PwmLight(4, light_settings.get("on"), light_settings.get("brightness"))

app = Microdot()


@app.get("/")
async def state_handler(request):
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


def connect_to_network(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xA11140)

    wlan.connect(ssid, password)

    max_wait = 30
    for _ in range(0, max_wait):
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        print("waiting for connection...")
        onboard_led.toggle()
        time.sleep(0.3)

    if wlan.status() != 3:
        led.value(1)
        raise RuntimeError(
            "network connection failed, error code: " + str(wlan.status())
        )
    else:
        status = wlan.ifconfig()
        print("connected, ip = " + status[0])
        onboard_led.value(0)

print("Connecting to network")
connect_to_network(wifi_settings.get("ssid"), wifi_settings.get("pass"))


async def main():
    await app.start_server(port=80, debug=True)


asyncio.run(main())
