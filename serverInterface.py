import paho.mqtt.client as mqtt
from datetime import datetime
import json

class Serverwriter:
    ### Initializes the connection to the light component
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect("0.tcp.eu.ngrok.io", 11252)

        #self.serverIP = "127.0.0.1"

    # From https://www.raspberrypi-spy.co.uk/2012/09/getting-your-raspberry-pi-serial-number-using-python/
    def getserial(self):
        # Extract serial from cpuinfo file
        cpuserial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                 if line[0:6]=='Serial':
                    cpuserial = line[10:26]
            f.close()
        except:
            cpuserial = "ERROR000000000"
        
        return cpuserial

    ### Turns on the light
    def sendToServer(self, startTime:datetime, endTime:datetime, positionID:int):
        #serial = self.getSerial()
        serial = "p1kk3m4nd8008bs6969"
        combined_str = {"deviceId": serial, "startTime": str(startTime), "endTime": str(endTime), "positionId": positionID} # {string, datetime, datetime, int}
        self.json_msg = json.dumps(combined_str)
        print("Sending To Server: " + json.dumps(combined_str))
        self.client.publish("database", self.json_msg)  # Publishes to server

    def sendAlarm(self, alarmTime:datetime, positionId:int):
        #serial = self.getSerial()
        serial = "p1kk3m4nd8008bs6969"
        combined_str = {"deviceId": serial, "alarmTime": str(alarmTime), "positionId": positionId} # {string, datetime, datetime, int}
        self.json_msg = json.dumps(combined_str)
        print("Sending Data To Server")
        self.client.publish("database", self.json_msg)  # Publishes to server

#server = Serverwriter()
#server.sendToServer("Test of data")
