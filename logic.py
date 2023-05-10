import threading
from datetime import datetime
from serverInterface import Serverwriter
from queue import Queue
from time import sleep

from stateMachine import LightMachine

class MonitorMovement:
    ### Initializes the components of this class
    def __init__(self, sensors, controller):
        self.sensors = sensors
        self.lc = controller
        self.lm = LightMachine(self.lc)
        self.server = Serverwriter()

        self.activeState = False
        self.thread = None
        self.epoch_time = datetime.now()


    ### Will return the time from last time
    def delta(self, t1, t2):
        delta = (t2 - t1)
        return int(delta.total_seconds())


    def activate(self):
        self.activeState = True
        self.thread = threading.Thread(target=self.monitorMovementV2)
        self.thread.start()


    def deactivate(self):
        self.activeState = False
        self.thread.join()


    def monitorMovementV2(self):
        latest = -1
        prev = -1
        start_time = -1
        end_time = -1
        
        while True: #self.activeState
            sleep(1)
            latest = self.mostRecent()

            # should run if latest sensor is different from the previous sensor or the time since reading is over 2 sek
            if (latest != prev or (self.delta(self.readSensorData(latest), datetime.now()) > 60)): 
                end_time = datetime.now()
                if end_time != -1 and start_time != -1:
                    print("sending to server")
                    self.server.sendToServer(start_time, end_time, prev)
                    start_time = -1
                    end_time = -1

                if(latest == 0):
                    self.lm.trigger_sens_bed()
                elif(latest == 1):
                    self.lm.trigger_sens1()
                elif(latest == 2):
                    self.lm.trigger_sens2()
                elif(latest == 3):
                    self.lm.trigger_sens3()
                elif(latest == 4):
                    self.lm.trigger_sens4()

                start_time = datetime.now()

            # If it has been more than 5 minutes all of the light should turn on
            elif (not (latest == 0) and (self.delta(self.readSensorData(latest), datetime.now() )> 20)):
                self.server.sendAlarm(start_time, latest)
                self.lm.trigger_alarm()

            prev = latest

    def mostRecent(self):
        reading = self.readSensorData(0)

        smallest_value = reading
        smallest_index = 0

        for i in range(len(self.sensors)):
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
                