import paho.mqtt.client as mqtt
from datetime import datetime
import paramiko
from time import sleep
import json

class Serverwriter:
    ### Initializes the connection to the light component
    def __init__(self):
        self.client = mqtt.Client()
        IP, PORT = self.get_mqtt_broker_ip()
        self.client.connect(IP, PORT)

    # From https://www.raspberrypi-spy.co.uk/2012/09/getting-your-raspberry-pi-serial-number-using-python/
    ### Returns the individual PI serial number
    def getSerial(self):
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

    ### Sends message with start time end time and sensor location
    def sendToServer(self, startTime:datetime, endTime:datetime, positionID:int):
        serial = self.getSerial()
        combined_str = {"deviceId": serial, "startTime": str(startTime), "endTime": str(endTime), "positionId": positionID} # {string, datetime, datetime, int}
        self.json_msg = json.dumps(combined_str)
        print("Sending To Server: " + json.dumps(combined_str))
        self.client.publish("database", self.json_msg)  # Publishes to server

    ### Sends accident time and position
    def sendAlarm(self, alarmTime:datetime, positionId:int):
        serial = self.getSerial()
        combined_str = {"deviceId": serial, "alarmTime": str(alarmTime), "positionId": positionId} # {string, datetime, datetime, int}
        self.json_msg = json.dumps(combined_str)
        print("Sending Alarm To Server: " + json.dumps(combined_str))
        self.client.publish("database", self.json_msg)  # Publishes to server

    ### Returns the IP and PORT of server
    def get_mqtt_broker_ip(self):
        # define the remote host and username
        hostname = "analogskilte.dk"
        username = "api"

        # create a new SSH client object
        client = paramiko.SSHClient()

        # automatically add the host key if it is unknown
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # load the private key from the local machine
        private_key_file = "/home/cep2/.ssh/id_rsa"
        private_key = paramiko.RSAKey.from_private_key_file(private_key_file)

        # connect to the remote host using key-based authentication
        client.connect(hostname, username=username, pkey=private_key)
        #cat mqtt.txt
        command = "cat /home/api/links/mqtt.txt"

        stdin, stdout, stderr = client.exec_command(command)

        # print the command output
        if  out := stdout.read().decode('utf-8'):
            print("Previous stdout: ", out,"\n")
        
        if  err := stderr.read().decode('utf-8'):
            print("stderr: ", err)


        #restart links service
        command = "sudo systemctl restart links.service"
        stdin, stdout, stderr = client.exec_command(command)

        if  out := stdout.read().decode('utf-8'):
            print("stdout: ", out,"\n")
        
        if  err := stderr.read().decode('utf-8'):
            print("stderr: ", err)

        #get links service status
        command = "sudo systemctl status links.service"
        stdin, stdout, stderr = client.exec_command(command)

        if  out := stdout.read().decode('utf-8'):
            print("stdout: ", out,"\n")
        
        if  err := stderr.read().decode('utf-8'):
            print("stderr: ", err)


        sleep(2)
        #cat mqtt.txt
        command = "cat /home/api/links/mqtt.txt"

        stdin, stdout, stderr = client.exec_command(command)

        # print the command output
        if  out := stdout.read().decode('utf-8'):
            print("stdout: ", out,"\n")
        
        if  err := stderr.read().decode('utf-8'):
            print("stderr: ", err)


        # define the path to the remote file to copy
        remote_file_path = "/home/api/links/mqtt.txt"

        # open the remote file and read its contents into a variable
        with client.open_sftp().file(remote_file_path, "r") as remote_file:
            file_contents = remote_file.read()

        # close the SSH connection
        client.close()

        # print the contents of the file
        print(file_contents.decode('utf-8'))
        string = file_contents.decode('utf-8')
        split_string = string.split(":")  # Split the string at the colon

        IP = split_string[0]  # Get the string before the colon
        PORT = int(split_string[1])  # Get the integer after the colon and convert it to int
        return (IP, PORT)


