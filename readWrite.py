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
        self.queue = Queue()                # Queues to push the sensor data into 
        self.new_message = False            # boolean to keep track wether or not there's a new message

        # ## Logic to start the loop of threads
        # client = mqtt.Client()              # Initializes the mqtt client
        # client.on_message = self.on_message # calls the on_message function, when sensor detects motion
        # self.sensorVal = client.on_message  # sensorval gets updated on message
        # client.connect("localhost", 1883)   # connects the client
        # client.subscribe(self.name)         # connects to the passed name (sensors firnedly name) "zigbee2mqtt/0x00158d000572a63f"
        # client.loop_start()                 # Initialises the loop (Important to stop the loop when finished)
    
    # ### on_message put time signatures into the queue, is called everytime sensor motion is detected
    # def on_message(self, client, userdata, msg):
    #     payload = msg.payload.decode('utf-8')
    #     # data = json.loads(payload)
    #     if True: #("illuminance" in payload  or "occupancy" in payload):# in data               # will check if illuminance is present in the data recieved, as this will prevent from loading errors
    #         print("Message recieved")           # prints to console
    #         self.new_message = True
    #         now = datetime.now()                
    #         self.queue.put(now)                     # put the time of the sensor reading into the queue
    
    ### The getData returns the latest time stamp that the sensor was activated
    def getData(self):
        while not self.queue.empty():           # will run through untill the most recent input of the queue
            self.sensorVal = self.queue.get()   # updates sensorval
        self.new_message = False
        return self.sensorVal               # return the latest time 

    ### Terminates the loops on each thread
    def terminate(client, userdata, rc=0):
        logging.debug("DisConnected result code "+str(rc))
        ### Terminates the thread
        client.loop_stop()

    ### Function to manipulate a sensor reading for testing
    def manipulate_sensor_reading(self):
        print("Message recieved")           # prints to console
        self.new_message = True
        now = datetime.now()                
        self.queue.put(now)

    
class Light:
    def __init__(self, name):
        self.name = name

        broker_address = "localhost"
        broker_port = 1883
        self.client = mqtt.Client()
        self.client.connect(broker_address, broker_port)

        self.state = False
    
    def publish(self, message):
        self.client.publish(self.name, message) 
    
    def get_state(self):
        return self.state
    
    def set_state(self, s: bool):
        self.state = s


class LightController:
    ### Initializes the connection to the light component
    def __init__(self):
        # message to pass for off
        broker_out_off = {"state":"OFF"}
        self.data_out_off = json.dumps(broker_out_off)

        # message to pass for alarm
        data_alarm = {"state": "ON", "color":{"r":255,"g":0,"b":0}}
        self.data_alarm = json.dumps(data_alarm)

        # array containing the lights
        self.lights = []

    # Function for getting color dictionary
    def get_color_dictionary(color_key):
        colors = {
            'red': {'r': 255, 'g': 0, 'b': 0},
            'green': {'r': 0, 'g': 255, 'b': 0},
            'blue': {'r': 0, 'g': 0, 'b': 255},
            'white': {'r': 255, 'g': 255, 'b': 255}
        }

        if color_key in colors:
            color_value = colors[color_key]
            color_dict = {
                'state': 'ON',
                'color': {
                    'r': color_value['r'],
                    'g': color_value['g'],
                    'b': color_value['b']
                }
            }
        else:
            # White if not recognized
            color_dict = {
                'state': 'ON',
                'color': {
                    'r': color_value['r'],
                    'g': color_value['g'],
                    'b': color_value['b']
                }
            }
        return color_dict

    ### add a new light
    def add_light(self, adress):
        light = Light(adress)
        self.lights.append(light)

    ### Turns on the light with ID and color
    def turnOn(self, ID, color: str):
        self.lights[ID].set_state(True)
        message = json.dumps(self.get_color_dictionary(color))
        self.lights[ID].publish(message)
        

    ### Turns off the ligh with ID; IDt
    def turnOff(self, ID):
        self.lights[ID].set_state(False)
        message = self.data_out_off                 # Message to turn off
        self.lights[ID].publish(message)     # Publishes to self.name aka topic

    def alarm(self):
        for light in self.lights:
            light.set_state(True)
            message = self.data_alarm
            light.publish(message)
    
    ### Terminates the connection
    def terminate(self, client):
        client.disconnect()                 # Disconnects the client

    def activeLights(self):
        active = []
        for index, light in enumerate(self.lights):
            if light.get_state() == True:
                active.append(index)
        return active
    


# sensor = SensorRead("test")
# sensor.manipulate_sensor_reading()
# print(sensor.new_message)
# print(sensor.getData())
# print(sensor.new_message)
