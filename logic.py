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

        self.activeState = False
        self.thread = None


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

    def activate(self):
        self.activeState = True
        self.thread = threading.Thread(target=self.monitorMovementV2)
        self.thread.start()

    def deactivate(self):
        self.activeState = False
        self.thread.join()

    def monitorMovementV2(self):
        while True: #self.activeState
            latest = self.mostRecent()
            print(latest)
            
            # should run if latest sensor is different from the previous sensor or the time since reading is over 2 sek
            if (not (latest == prev) or self.delta(self.readSensorData(latest) > 2)): 
                if(latest == 0):
                    print("should trigger bed")
                    self.lm.trigger_bed()
                elif(latest == 1):
                    self.lm.trigger_sens1()
                elif(latest == 2):
                    self.lm.trigger_sens2()
                elif(latest == 3):
                    self.lm.trigger_sens3()

            elif (not (latest == 0) and self.delta(self.readSensorData(latest) > 20)):
                self.lm.trigger_alarm()
                  
            prev = latest
            sleep(1)
            
            

    def mostRecent(self):
        reading = self.readSensorData(0)
        if not type(reading) == type(self.epoch_time):
            return -1
        smallest_value = reading
        smallest_index = 0
        
        for i in range(len(self.sensors)):
            if not type(reading) == type(self.epoch_time):
                continue    
            if self.delta(self.readSensorData(i), smallest_value) < 0:
                smallest_value = self.readSensorData(i)
                smallest_index = i
        return smallest_index
    
    ### Gets the latest output from the sensor (In datetime)
    def readSensorData(self, ID):
        sensor = self.sensors[ID]
        if not type(sensor.getData()) == type(self.epoch_time):
                return datetime(1970, 1, 1)    
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

