import threading
from datetime import datetime
from serverInterface import Serverwriter
from queue import Queue
from time import sleep

from stateMachine import LightMachine

class MonitorMovement:
    ### Initializes the components of this class
    def __init__(self, sensors, controller):
        self.monitorState = False
        self.sensors = sensors
        self.lc = controller
        self.lock = threading.Lock()

        self.epoch_time = datetime.now()

        self.server = Serverwriter

        self.lm = LightMachine(self.lc)


    ### Will return the time from last time
    def delta(self, t1, t2):
        delta = (t2 - t1)
        return int(delta.total_seconds())

    ### Logic for when and which lights to turn on
    def monitorMovement(self):
        controller = self.lc
        while True:
            reading = self.readSensorData(0)    # Time Reading
            now = datetime.now()

            # If there's no time return from get_data
            if not type(reading) == type(self.epoch_time):
                continue


            delta = self.delta(reading, now)
            print(f"Time since Reading: {delta}")
            if 20 < delta:
                controller.alarm(0)
            elif delta < 10:
                self.epoch_time = reading
                controller.turnOn(0)

                self.server.sendToServer(self.epoch_time)
                
            else: 
                controller.turnOff(0)
            sleep(1)

    def monitorMovementV2(self):
        while True:
            sm = self.lm
            if(self.mostRecent() == 0):
                sm.trigger_bed
            elif(self.mostRecent() == 1):
                sm.trigger_sens1
            elif(self.mostRecent() == 2):
                sm.trigger_sens2
            elif(self.mostRecent() == 3):
                sm.trigger_sens3
            
            

    def mostRecent(self):
        if len(self.sensors) == 0:
            return -1
        smallest_value = self.sensors[0]
        smallest_index = 0
        for i in range(1, len(self.sensors)):
            if self.sensors[i] < smallest_value:
                smallest_value = self.sensors[i]
                smallest_index = i
        return smallest_index
    
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
    

    def terminate(self):
        for i in self.lights:
            self.lights[i].terminate()
        for i in self.sensors:
            self.sensors[i].terminate()
