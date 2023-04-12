from readWrite import SensorRead
from readWrite import LightController
from logic import MonitorMovement
from datetime import datetime

from time import sleep

sensor_1 = SensorRead("zigbee2mqtt/0x00158d000572a63f")

sensors = []
sensors.append(sensor_1)

led_1 = LightController("zigbee2mqtt/0xbc33acfffe8b8d7c/set")
led_1.turnOff()
lights = []
lights.append(led_1)

monitor = MonitorMovement(sensors, lights)
monitor.monitorMovement()



print("Hello World!")

start_time = datetime.time(23, 0)
end_time = datetime.time(7, 0)
"""
# Checks if the first sensor is the most recent activated
def isMostRecent():
    is_recent = True
    for i in range(1, len(sensors)):
        if sensors[i] < sensors[0]:
            is_recent = False
            break
    return is_recent

def main():
    while True:
        if datetime.now() >= start_time and datetime.now() <= end_time:
            if isMostRecent():
                
                pass

        


if __name__ == "__main__":
    main()
"""
