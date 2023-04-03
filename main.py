from readWrite import SensorRead
from readWrite import LightController
from logic import MonitorMovement

from time import sleep

sensor_1 = SensorRead("zigbee2mqtt/0x00158d000572a63f", 0)

sensors = []
sensors.append(sensor_1)

led_1 = LightController("zigbee2mqtt/0xbc33acfffe8b8d7c/set", 0)
led_1.turnOff()
lights = []
lights.append(led_1)

monitor = MonitorMovement(sensors, lights)
monitor.monitorMovement()

sensor_1.terminate()
led_1.terminate()

print("Hello World!")

