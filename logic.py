import threading
from datetime import datetime
from queue import Queue
from time import sleep

class MonitorMovement:
    ### Initializes the components of this class
    def __init__(self, sensors, lights):
        self.monitorState = False
        self.sensors = sensors
        self.lights = lights
        self.lock = threading.Lock()

        self.epoch_time = datetime.now()

    ### Will return the time from last time
    def delta(self, now):
        delta = (now - self.epoch_time)
        return int(delta.total_seconds())

    ### Logic for when and which lights to turn on
    def monitorMovement(self):
        
        self.lightWrite(0, False)
        while True:
            reading = self.readSensorData(0)
            if not type(reading) == type(self.epoch_time):
                continue
            #self.epoch_time = self.readSensorData(0)
            print(f"Time since Reading: {self.delta(reading)}")
            if self.delta(reading) > 10:
                self.lightWrite(0, True)
            else:
                self.lightWrite(0, False)
            self.epoch_time = reading
            sleep(1)





    
    ### Gets the latest output from the sensor (In datetime)
    def readSensorData(self, ID):
        sensor = self.sensors[ID]
        return sensor.getData()
                

    def sendData():
        x = 0
    
    ###  Changes monitorState to the opposite
    def stateMonitoring():
        if(monitorState):
            monitorState = False
        else:
            monitorState = True
    
    ### function to turn a specifik light on or off
    def lightWrite(self, ID, state):
        light = self.lights[ID]

        # if the state that is passed to the ID is true turn on
        if state:
            light.turnOn()

        # if the state passed is false turn of the light 
        if not state:
            light.turnOff()


