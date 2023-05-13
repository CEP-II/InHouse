import paramiko
from time import sleep

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
