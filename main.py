from readWrite import SensorRead
from readWrite import LightController
from logic import MonitorMovement
from datetime import date, datetime, time, timedelta
from serverInterface import Serverwriter

from time import sleep
server = Serverwriter()



# returns the index of the most recent active sensor
def mostRecent():
    if len(sensors) == 0:
        return -1
    smallest_value = sensors[0]
    smallest_index = 0
    for i in range(1, len(sensors)):
        if sensors[i] < smallest_value:
            smallest_value = sensors[i]
            smallest_index = i
    return smallest_index

sensor_1 = SensorRead("zigbee2mqtt/0x00158d000572a63f")
sensor_2 = SensorRead("zigbee2mqtt/0x00158d00054a6fcb")

sensors = []
sensors.append(sensor_1)
sensors.append(sensor_2)

controller = LightController()
controller.add_light("zigbee2mqtt/0xbc33acfffe8b8d7c/set")
controller.add_light("zigbee2mqtt/0x680ae2fffebe8c38/set")
controller.turnOff(0)

monitor = MonitorMovement(sensors, controller)
#monitor.monitorMovement()

def get_start_time():
    today = datetime.today()
    start = time(15,50,0)
    start_time = datetime.combine(today,start)
    return start_time

def get_end_time():
    tomorrow = datetime.today() + timedelta(days = 1)
    end = time(7,0,0)
    end_time = datetime.combine(tomorrow,end)
    #Return for testing purposes
    end_time = get_start_time() + timedelta(minutes=10)
    return  end_time

def main():
    monitor_state = False
    start_time = get_start_time()
    end_time = get_end_time()
    print(start_time)
    print(end_time)

    while True:
        if not monitor_state: #If the monitor state is off it should run
            #Will check if we are in the correct time frame
            print("Checks to see if time is right")
            print(datetime.now())
            if datetime.now() >= start_time and datetime.now() <= end_time:
                #Will then check if the last activated sensor is from the bedroom
                print("timeframe right")
                if mostRecent() == 0:
                    print("bedroom is most recent sensor")
                    print("monitor state = true")
                    monitor_state = True

                    pass
            print("Time out of bounds, sleep 10")
            sleep(10) # Will only check every 60 seconds

        elif datetime.now() > end_time:
            print("Past end-time")
            monitor_state = False #If the time exceeds 7 am it will turn off the monitoring
            start_time = get_start_time()
            end_time = get_end_time()

        else:
            #monitor.monitorMovement()
            print("monitoring")
            server.sendToServer({1:'Hello World'})
            sleep(10)
                
            
            

        


if __name__ == "__main__":
    main()

