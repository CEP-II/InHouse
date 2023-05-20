from readWrite import SensorRead
from readWrite import LightController
from logic import MonitorMovement
from datetime import datetime, time, timedelta
from time import sleep
import math

def get_start_time():
    today = datetime.today()
    start = time(22,0,0)
    start_time = datetime.combine(today,start)
    return start_time

def get_end_time():
    tomorrow = datetime.today() + timedelta(days = 1)
    end = time(0,0,0)
    end_time = datetime.combine(tomorrow,end)
    return  end_time

def main():
    sleep(2)
    sensors = []
    sensor_bed = SensorRead("zigbee2mqtt/0x00158d000572a63f")
    sensor_1 = SensorRead("zigbee2mqtt/0x00158d00054a6fcb")
    #sensor_2 = SensorRead("zigbee2mqtt/0x842e14fffe571021")
    sensor_2 = SensorRead("zigbee2mqtt/0x00158d0007e3d31f")
    #sensor_3 = SensorRead("zigbee2mqtt/0xbc33acfffe167e53")    
    sensor_3 = SensorRead("zigbee2mqtt/0x00158d0007e4153d")
    #sensor_bath = SensorRead("zigbee2mqtt/0xbc33acfffe184596")
    sensor_bath = SensorRead("zigbee2mqtt/0x00158d0007e22215")

    sensors.append(sensor_bed)
    sensors.append(sensor_1)
    sensors.append(sensor_2)
    sensors.append(sensor_3)
    sensors.append(sensor_bath)
    
    controller = LightController()
    controller.add_light("zigbee2mqtt/0xbc33acfffe8b8d7c/set")
    controller.add_light("zigbee2mqtt/0x680ae2fffebe8c38/set")
    controller.add_light("zigbee2mqtt/0x680ae2fffec0ccb7/set")
    controller.add_light("zigbee2mqtt/0xcc86ecfffebfaefc/set")
    
    controller.turnOff(0)
    controller.turnOff(1)
    controller.turnOff(2)
    controller.turnOff(3)

    monitor = MonitorMovement(sensors, controller)

    start_time = get_start_time()
    end_time = get_end_time()
    print("end time: " + str(end_time))

    # Loop that will always run
    while True:
        sleep(3)
        if not monitor.activeState: #monitor_state: #If the monitor state is off it should run
            #Will check if we are in the correct time frame
            if monitor.mostRecent() == 0:
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
                    # will sleep half of the time left to start time
                    print("Time out of bounds, sleep 10")
                    time_diff = (start_time - datetime.now()).total_seconds()
                    time_to_sleep = math.florr(0.5*(time_diff))
                    print(f"will sleep {time_to_sleep} seconds")
                    sleep(time_to_sleep) 
            else:
                sleep(2)
        
        elif datetime.now() > end_time:
            print("Past end-time")
            monitor.deactivate()
            start_time = get_start_time()
            end_time = get_end_time()
            

        else:
            print("monitoring")
            # sensor_bed.manipulate_sensor_reading()
            # sleep(5)
            # sensor_1.manipulate_sensor_reading()
            # sleep(150)
            # sensor_2.manipulate_sensor_reading()
            # sleep(5)
            # sensor_3.manipulate_sensor_reading()
            # sleep(5)
            # sensor_bath.manipulate_sensor_reading()
            # sleep(5)
            # sensor_bath.manipulate_sensor_reading()
            # sleep(5)
            # sensor_3.manipulate_sensor_reading()
            # sleep(5)
            # sensor_2.manipulate_sensor_reading()
            # sleep(5)
            # sensor_1.manipulate_sensor_reading()
            # sleep(5)
            # sensor_bed.manipulate_sensor_reading()
            # sleep(5)
            # sensor_1.manipulate_sensor_reading()
            # sleep(20)
            sleep(60)
            

if __name__ == "__main__":
    main()

