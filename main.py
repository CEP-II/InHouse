from readWrite import SensorRead
from readWrite import LightController
from logic import MonitorMovement
from datetime import date, datetime, time, timedelta

from time import sleep



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

sensors = []
sensors.append(sensor_1)

controller = LightController()
controller.add_light("zigbee2mqtt/0xbc33acfffe8b8d7c/set")
controller.turnOff(0)

monitor = MonitorMovement(sensors, controller)
#monitor.monitorMovement()

def get_start_time():
    today = datetime.today()
    start = time(17,29,0)
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

        else:
            #monitor.monitorMovement()
            print("monitoring")
                
            
            

        


if __name__ == "__main__":
    main()

