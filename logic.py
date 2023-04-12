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
    def delta(self, t1, t2):
        delta = (t2 - t1)
        return int(delta.total_seconds())

    ### Logic for when and which lights to turn on
    def monitorMovement(self):
        self.lightWrite(0, False)

        while True:
            reading = self.readSensorData(0)    # Time Reading
            now = datetime.now()

            # If there's no time return from get_data
            if not type(reading) == type(self.epoch_time):
                continue


            delta = self.delta(reading, now)
            print(f"Time since Reading: {delta}")
            if 20 < delta:
                print("alarm")
                light = self.lights[0]
                light.alarm()
                self.terminate()
                break
            elif delta < 10:
                self.epoch_time = reading
                self.lightWrite(0, True)
            else: 
                self.lightWrite(0, False)
            sleep(1)

    def monitorMovementV2(self):
        while True:
            return

    
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

    def terminate(self):
        for i in self.lights:
            self.lights[i].terminate()
        for i in self.sensors:
            self.sensors[i].terminate()
