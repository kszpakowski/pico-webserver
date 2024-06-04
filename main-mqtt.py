import network
import time
import json
import _thread

from lights import PwmLight
from settings import Settings

from machine import Pin
from umqtt.simple import MQTTClient

id = machine.unique_id().hex()


onboard_led = Pin("LED", Pin.OUT)
wifi_settings = Settings("wifi")

light_settings = Settings("light", {"on": False, "brightness": 100})
light = PwmLight(4, light_settings.get("on"), light_settings.get("brightness"))


def status_updater():
    while True:
        mqtt_client.wait_msg()


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
        # led.value(1)
        raise RuntimeError(
            "network connection failed, error code: " + str(wlan.status())
        )
    else:
        status = wlan.ifconfig()
        print("connected, ip = " + status[0])
        onboard_led.value(0)


def mqtt_subscription_callback(topic, message):
    print(
        f"Topic {topic} received message {message}"
    )  # Debug print out of what was received over MQTT
    data = json.loads(message)

    if "on" in data:
        on = data["on"]
        print(on)
        if on:
            light.turn_on()
        else:
            light.turn_off()
    if "brightness" in data:
        light.set_brightness(data["brightness"])


print("Connecting to network")
connect_to_network(wifi_settings.get("ssid"), wifi_settings.get("pass"))

mqtt_client = MQTTClient(client_id=id, server="192.168.1.86", port=30007)

# Before connecting, tell the MQTT client to use the callback
mqtt_client.set_callback(mqtt_subscription_callback)

mqtt_client.connect()

mqtt_client.subscribe("devices/" + id)

_thread.start_new_thread(status_updater, ())

print("Subscribed")

try:
    while True:
        json_str = json.dumps({"id": id, "state": light.get_state()})

        mqtt_client.publish("devices", json_str)

        time.sleep(1)

except Exception as e:
    print(f"Failed to publish message: {e}")
finally:
    mqtt_client.disconnect()
