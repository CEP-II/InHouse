from readWrite import SensorRead
from time import sleep

sensor_1 = SensorRead("zigbee2mqtt/0x00158d000572a63f", 0)

sensor_2 = SensorRead("zigbee2mqtt/0x00158d000572a63f", 1)

i = 0
while(i < 100):
    sensor_1.getData()
    sensor_2.getData()
    sleep(1)
    i = i + 1

sensor_1.terminate()
sensor_2.terminate()
print("Hello World!")

