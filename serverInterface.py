import paho.mqtt.client as mqtt
import json

class Serverwriter:
    ### Initializes the connection to the light component
    def __init__(self, message):
        self.message = json.dumps(message)  

        self.client = mqtt.Client()
        self.client.connect("localhost", 1883)

        self.serverIP = "127.0.0.1"

    ### Turns on the light
    def sendToServer(self):
        print("Sending Data To Server")
        self.client.publish(self.serverIP, self.message)  # Publishes to server
