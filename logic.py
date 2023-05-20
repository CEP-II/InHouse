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

    ### Starts the thread
    def activate(self):
        self.activeState = True
        self.thread = threading.Thread(target=self.monitorMovement)
        self.thread.start()

    ### teminates the thread
    def deactivate(self):
        self.activeState = False
        if self.thread and self.thread.is_alive():
            self.thread.join()



    def monitorMovement(self):
        start_time = -1
        end_time = datetime.now()
        alarm = False
        latest = -1
          
        while self.activeState: 
            sleep(1)
            for index, sensor in enumerate(self.sensors):
                if index == latest and self.delta(end_time, datetime.now()) < 5:
                    self.readSensorData(index)
                    continue
                if sensor.new_message:
                    end_time = self.readSensorData(index)

                    print("\n")
                    print("New signal from sensor: " + str(index))

                    if start_time != -1:
                        self.server.sendToServer(start_time, end_time, latest)
                        start_time = -1

                    if(index == 0):
                        self.lm.trigger_sens_bed()
                        start_time = -1
                    elif(index == 1):
                        self.lm.trigger_sens1()
                    elif(index == 2):
                        self.lm.trigger_sens2()
                    elif(index == 3):
                        self.lm.trigger_sens3()
                    elif(index == 4):
                        self.lm.trigger_sens4()

                    start_time = datetime.now()
                    latest = index
                    
                    print("\n")

                elif not alarm and latest != 0 and latest != 4 and (self.delta(end_time, datetime.now()) > 120):
                    self.server.sendAlarm(start_time, latest)
                    self.lm.trigger_alarm()
                    self.readSensorData(index)
                    alarm = True
                    return


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
                