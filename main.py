from readWrite import SensorRead
from readWrite import LightController
from logic import MonitorMovement
from datetime import date, datetime, time, timedelta
from serverInterface import Serverwriter
from time import sleep

def get_start_time():
    today = datetime.today()
    start = time(16,55,0)
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
    sensor_bed = SensorRead("zigbee2mqtt/0x00158d000572a63f")
    sensor_1 = SensorRead("zigbee2mqtt/0x00158d00054a6fcb")
    sensor_2 = SensorRead("zigbee2mqtt/0x842e14fffe571021")
    sensor_3 = SensorRead("zigbee2mqtt/0xbc33acfffe167e53")
    sensor_bath = SensorRead("zigbee2mqtt/0xbc33acfffe184596")

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

    controller.turnOn(0, "white")
    sleep(1)
    controller.turnOn(1, "white")
    sleep(1)
    controller.turnOn(2, "white")
    sleep(1)
    controller.turnOn(3, "white")
    sleep(1)

    # controller.turnOff(0)
    # controller.turnOff(1)
    # controller.turnOff(2)
    # controller.turnOff(3)

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
                    print("Time out of bounds, sleep 10")
                    sleep(10) # Will only check every 60 seconds
            else:
                sleep(2)
        
        elif datetime.now() > end_time:
            print("Past end-time")
            #monitor_state = False #If the time exceeds 7 am it will turn off the monitoring
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
            # #monitor.monitorMovementV2()
            # #server.sendToServer({1:'Hello World'})
            sleep(60)
            
            
            

        


if __name__ == "__main__":
    main()

