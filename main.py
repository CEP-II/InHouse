from readWrite import SensorRead
from readWrite import LightController
from logic import MonitorMovement
from datetime import date, datetime, time, timedelta
from serverInterface import Serverwriter

from time import sleep


#server = Serverwriter()



# returns the index of the most recent active sensor
def mostRecent(sensors):
    #precondition is that there are at least 1 sensor in the array
    if len(sensors) == 0:
        return -1
    
    sensor = sensors[0]
    print(type(sensor.getData()))
    print(type(get_start_time()))
    
    # if the sensors hasn't had time to update fully it won't have the right type
    # this if statements assures that, and otherwise it will return -1
    if not type(sensor.getData()) == type(get_start_time()):
        smallest_value = datetime(1970, 1, 1)
        smallest_index = -1
    else:
        smallest_value = sensor.getData()
        smallest_index = 0
       
    for i in range(1, len(sensors)):
        sensor = sensors[i]

        if not type(sensor.getData()) == type(get_start_time()):
            continue 
        
        if sensor.getData() < smallest_value:
            smallest_value = sensor.getData()
            smallest_index = i

    return smallest_index



def get_start_time():
    today = datetime.today()
    start = time(17,48,0)
    start_time = datetime.combine(today,start)
    return start_time

def get_end_time():
    tomorrow = datetime.today() + timedelta(days = 1)
    end = time(7,0,0)
    end_time = datetime.combine(tomorrow,end)
    #Return for testing purposes
    end_time = get_start_time() + timedelta(minutes=80)
    return  end_time

def main():
    sensors = []
    sensor_1 = SensorRead("zigbee2mqtt/0x00158d000572a63f")
    sensor_2 = SensorRead("zigbee2mqtt/0x00158d00054a6fcb")
    sensors.append(sensor_1)
    sensors.append(sensor_2)

    controller = LightController()
    controller.add_light("zigbee2mqtt/0xbc33acfffe8b8d7c/set")
    controller.add_light("zigbee2mqtt/0x680ae2fffebe8c38/set")

    controller.turnOff(0)
    controller.turnOff(1)

    monitor = MonitorMovement(sensors, controller)

    monitor_state = False
    start_time = get_start_time()
    end_time = get_end_time()
    
    # Loop that will always run
    while True:
        if not  monitor.activeState: #monitor_state: #If the monitor state is off it should run
            #Will check if we are in the correct time frame
            if mostRecent(sensors) == 0:
                print("bedroom is most recent sensor")
                print("Checks to see if time is right")
                print(datetime.now())
                if datetime.now() >= start_time and datetime.now() <= end_time:
                    #Will then check if the last activated sensor is from the bedroom
                    print("timeframe right")
                    print("monitor state = true")
                    #monitor_state = True
                    monitor.activate()
                    pass
                else:
                    print("Time out of bounds, sleep 10")
                    sleep(10) # Will only check every 60 seconds
            else:
                print(mostRecent(sensors))
                sleep(1)

        elif datetime.now() > end_time:
            print("Past end-time")
            #monitor_state = False #If the time exceeds 7 am it will turn off the monitoring
            monitor.deactivate()
            start_time = get_start_time()
            end_time = get_end_time()

        else:
            #monitor.monitorMovement()
            print("monitoring")
            monitor.monitorMovementV2()
            #server.sendToServer({1:'Hello World'})
            sleep(10)
                
            
            

        


if __name__ == "__main__":
    main()

