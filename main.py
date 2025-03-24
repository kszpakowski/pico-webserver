import uasyncio as asyncio
import network
import time

# https://microdot.readthedocs.io/en/latest/index.html
from microdot import Microdot, Response

from lights import PwmLight
from settings import Settings

# Load Wi-Fi settings
wifi_settings = Settings("wifi")
wlan = network.WLAN(network.STA_IF)
app = Microdot()

# Load light settings
light_settings = Settings("light", {"on": False, "brightness": 100})
light = PwmLight(4, light_settings.get("on"), light_settings.get("brightness"))


async def wifi_monitor():
    """Monitor Wi-Fi connection and reconnect if lost."""
    ssid = wifi_settings.get("ssid")
    password = wifi_settings.get("pass")

    while True:
        if wlan.status() != 3:  # Not connected
            print("Wi-Fi disconnected! Attempting reconnection...")
            wlan.active(True)
            wlan.config(pm=0xA11140)
            wlan.connect(ssid, password)

            for i in range(20):  # Try for 10 seconds (20 x 0.5s)
                print(f"#{i} Connecting to {ssid} (Status: {wlan.status()})")
                if wlan.status() == 3:
                    print(f"Connected to {ssid} - {wlan.ifconfig()[0]}")
                    break
                await asyncio.sleep(0.5)  # Non-blocking sleep

        await asyncio.sleep(5)  # Check every 5 seconds


@app.get("/")
async def state_handler(_):
    """Handle GET requests to fetch light state."""
    state = light.get_state()
    return Response(body=state)


@app.put("/")
async def update_handler(request):
    """Handle PUT requests to update light settings."""
    data = request.json
    if "on" in data:
        if data["on"]:
            light.turn_on()
        else:
            light.turn_off()
    if "brightness" in data:
        light.set_brightness(data["brightness"])
    light_settings.save_settings(light.get_state())
    return Response(body={"status": "success"})


async def main():
    """Main function to start Wi-Fi monitor and web server."""
    asyncio.create_task(wifi_monitor())  # Run Wi-Fi monitor in background
    print("Starting Microdot server on port 80...")
    await app.start_server(port=80, debug=True)  # Start HTTP server


try:
    asyncio.run(main())  # Correctly start event loop
except KeyboardInterrupt:
    print("Server stopped")