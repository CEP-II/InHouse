import paho.mqtt.client as mqtt
from threading import Thread
import json
from queue import Queue
import logging
from time import sleep
from datetime import datetime

class SensorRead:
    ### Initializes name and value
    def __init__(self, name):
        self.name = name                    # individual name of each sensor
        self.sensorVal = datetime.now()     # Time stamp to pass
        self.queue = Queue()                    # Queues to push the sensor data into 

        ## Logic to start the loop of threads
        client = mqtt.Client()              # Initializes the mqtt client
        client.on_message = self.on_message # calls the on_message function, when sensor detects motion
        self.sensorVal = client.on_message  # sensorval gets updated on message
        client.connect("localhost", 1883)   # connects the client
        client.subscribe(self.name)         # connects to the passed name (sensors firnedly name) "zigbee2mqtt/0x00158d000572a63f"
        client.loop_start()                 # Initialises the loop (Important to stop the loop when finished)
    
    ### on_message put time signatures into the queue, is called everytime sensor motion is detected
    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8')
        # data = json.loads(payload)
        if "illuminance" in payload:# in data               # will check if illuminance is present in the data recieved, as this will prevent from loading errors
            print("Message recieved")           # prints to console
            now = datetime.now()                
            self.queue.put(now)                     # put the time of the sensor reading into the queue
    
    ### The getData returns the latest time stamp that the sensor was activated
    def getData(self):
        while not self.queue.empty():           # will run through untill the most recent input of the queue
            self.sensorVal = self.queue.get()   # updates sensorval
        
        return self.sensorVal               # return the latest time 

    ### Terminates the loops on each thread
    def terminate(client, userdata, rc=0):
        logging.debug("DisConnected result code "+str(rc))
        ### Terminates the thread
        client.loop_stop()

    
class Light:
    def __init__(self, name):
        self.name = name

        broker_address = "localhost"
        broker_port = 1883
        self.client = mqtt.Client()
        self.client.connect(broker_address, broker_port)
    
    def publish(self, message):
        self.client.publish(self.name, message) 


class LightController:
    ### Initializes the connection to the light component
    def __init__(self):
        # message to pass for on
        broker_out_on = {"state":"ON","color":{"r":255,"g":255,"b":255}}
        self.data_out_on = json.dumps(broker_out_on)

        # message to pass for off
        broker_out_off = {"state":"OFF"}
        self.data_out_off = json.dumps(broker_out_off)

        # message to pass for alarm
        data_alarm = {"state": "ON", "color":{"r":255,"g":0,"b":0}}
        self.data_alarm = json.dumps(data_alarm)

        # array containing the lights
        self.lights = []

    ### add a new light
    def add_light(self, adress):
        light = Light(adress)
        self.lights.append(light)

    ### Turns on the light with ID; ID
    def turnOn(self, ID):
        print("Turn On")
        message = self.data_out_on               # Message to turn on
        self.lights[ID].publish(message)         # turnOn message to the light with ID; ID

    ### Turns off the ligh with ID; IDt
    def turnOff(self, ID):
        print("Turn Off")
        message = self.data_out_off                 # Message to turn off
        self.lights[ID].publish(message)     # Publishes to self.name aka topic

    def alarm(self, ID):
        print("Alarm")
        message = self.data_alarm
        self.lights[ID]( message)
    
    ### Terminates the connection
    def terminate(self, client):
        client.disconnect()                 # Disconnects the client
    
    def lights_size(self):
        return len(self.lights)