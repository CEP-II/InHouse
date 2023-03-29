import paho.mqtt.client as mqtt
from threading import Thread
import json
import time
from time import sleep

class SensorRead:
    def __init__(self, name, val):
        ### Initializes thread
        super().__init__()
        self.daemon = True
        self.cancelled = False

        ### Initializes name and value
        self.name = name
        self.val = val

    def terminate(self):
        ### Terminates the thread
        self.cancelled = True

    def update(self):
        ### Updates counters
        pass

    def run(self):
        ### Will delay process in case of overrun thread
        while not self.cancelled:
            self.update()
            sleep(0.01)
    """
    def on_message(client, userdata, msg):
        message = json.loads(msg.payload)
        print(message["illuminance"])
        print(message)
        return message["illuminance"]

    def getData(self, client, userdata, msg):
        client = mqtt.Client()
        client.on_message = self.on_message
        client.connect("localhost", 1883)
        client.subscribe("zigbee2mqtt/0x00158d000572a63f")
        #client.loop_forever()
    """
    def getData(self):
        print(f"from {self.val}, time is {time.localtime()}")
        return time.localtime()


class LightController:
    x = 0
