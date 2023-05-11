import paramiko

# define the remote host and username
hostname = "analogskilte.dk"
username = "api"

# create a new SSH client object
client = paramiko.SSHClient()

# automatically add the host key if it is unknown
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# load the private key from the local machine
private_key_file = "/home/julius/.ssh/id_rsa.pub"
private_key = paramiko.RSAKey.from_private_key_file(private_key_file)

# connect to the remote host using key-based authentication
client.connect(hostname, username=username, pkey=private_key)

# define the path to the remote file to copy
remote_file_path = "/home/api/links/mqtt.txt"

# open the remote file and read its contents into a variable
with client.open_sftp().file(remote_file_path, "r") as remote_file:
    file_contents = remote_file.read()

# close the SSH connection
client.close()

# print the contents of the file
print(file_contents)
