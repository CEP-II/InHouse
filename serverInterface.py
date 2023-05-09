import paho.mqtt.client as mqtt
import json

class Serverwriter:
    ### Initializes the connection to the light component
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect("2.tcp.eu.ngrok.io", 15915)

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
    def sendToServer(self, startTime, endTime, positionID):
        serial = self.getSerial()
        combined_str = {"deviceId": serial, "startTime": startTime, "endTime": endTime, "positionID": positionID} # {string, datetime, datetime, int}
        self.json_msg = json.dumps(combined_str)
        print("Sending Data To Server")
        self.client.publish("database", self.json_msg)  # Publishes to server

#server = Serverwriter()
#server.sendToServer("Test of data")
