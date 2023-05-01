import pytest
from datetime import datetime
from nightguard.logic import MonitorMovement
from nightguard.readWrite import SensorRead, LightController
import threading
from queue import Queue
from time import sleep
import paho.mqtt.client as mqtt
from threading import Thread
import json
import logging





sensor_1 = SensorRead("zigbee2mqtt/0x00158d000572a63f", 0, "0.tcp.eu.ngrok.io")

sensors = []
sensors.append(sensor_1)

led_1 = LightController("zigbee2mqtt/0xbc33acfffe8b8d7c/set", 0,"0.tcp.eu.ngrok.io")
led_1.turnOff()
lights = []
lights.append(led_1)
a = MonitorMovement(sensors,lights)

@pytest.mark.parametrize("x, y, result", [
   (datetime.now(), datetime.now(), 0),
   
])


def test_delta(x, y, result):
  assert a.delta(x, y) is result
