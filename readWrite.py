import paho.mqtt.client as mqtt
from threading import Thread
import json
from queue import Queue
import logging
from time import sleep
from datetime import datetime

class SensorRead:
    ### Initializes name and value
    def __init__(self, name, ID):
        self.name = name        # individual name of each sensor
        self.val = ID          # ID for each sensor 
        self.sensorVal = datetime.now()      # Time stamp to pass
        self.q = Queue()        # Queues are thread-safe 

        ## Logic to start the loop of threads
        client = mqtt.Client()
        client.on_message = self.on_message
        self.sensorVal = client.on_message
        client.connect("localhost", 1883)
        client.subscribe(self.name) #"zigbee2mqtt/0x00158d000572a63f"
        client.loop_start()
    
    # on_message put time signatures into the queue
    def on_message(client, userdata, msg, self):
        now = datetime.now()
        message = json.loads(msg.payload)
        print(message["illuminance"])
        self.sensorVal = now
        self.q.put(now)
        #return now
    
    ### The getData returns the latest time sensor was activated
    def getData(self):
        while not self.q.empty():       #will run through untill the most recent input of the queue
            self.sensorVal = self.q.pop(0)
        
        return self.sensorVal

    ### Terminates the loops on each thread
    def terminate(client, userdata, rc=0):
        logging.debug("DisConnected result code "+str(rc))
        ### Terminates the thread
        client.loop_stop()

    

class LightController:
    ### Initializes the connection to the light component
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID

        broker_address = "localhost"
        broker_port = 1883
        client = mqtt.Client()
        client.connect(broker_address, broker_port)

        #ID's to pass for on and off
        broker_out_on = {"color":{"r":255,"g":255,"b":255}}
        self.data_out_on = json.dumps(broker_out_on)

        broker_out_off = {"color":{"r":0,"g":0,"b":0}}
        self.data_out_off = json.dumps(broker_out_off)

    ### Turns on the light
    def turnOn(self, client):
        message = self.data_out_on          # Message to turn on
        client.publish(message, self.name)  # Publishes to self.name aka topic

    ### Turns off the light
    def turnOff(self, client):
        message = self.data_out_off          # Message to turn off
        client.publish(message, self.name)   # Publishes to self.name aka topic
    
    ### Terminates the connection
    def terminate(self, client):
        client.disconnect()                 # Disconnects the client