import paho.mqtt.client as mqtt
import json

class Serverwriter:
    ### Initializes the connection to the light component
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect("192.168.204.52", 1883)

        #self.serverIP = "127.0.0.1"

    ### Turns on the light
    def sendToServer(self, message):
        self.message = json.dumps(message)  
        print("Sending Data To Server")
        self.client.publish("TEST", self.message)  # Publishes to server
