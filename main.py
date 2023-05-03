from readWrite import SensorRead
from readWrite import LightController
from logic import MonitorMovement
from datetime import datetime

import time
from time import sleep



# Checks if the first sensor / bedroom sensor is the most recent activated
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

led_1 = LightController("zigbee2mqtt/0xbc33acfffe8b8d7c/set")
led_1.turnOff()
lights = []
lights.append(led_1)

monitor = MonitorMovement(sensors, lights)
monitor.monitorMovement()

"""
start_time = datetime.time(23, 0)
end_time = datetime.time(7, 0)


monitor_state = False
def main():
    while True:
        if not monitor_state: #If the monitor state is off it should run
            #Will check if we are in the correct time frame
            if datetime.now() >= start_time and datetime.now() <= end_time:
                #Will then check if the last activated sensor is from the bedroom
                if mostRecent() == 0:
                    monitor_state = True
                    pass

            time.sleep(60) # Will only check every 60 seconds

        elif datetime.now() > end_time:
            monitor_state = False #If the time exceeds 7 am it will turn off the monitoring

        else:
            monitor.monitorMovement()
                
            
            

        


if __name__ == "__main__":
    main()

"""