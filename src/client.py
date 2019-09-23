import socket
import os
import threading

import utility

# Sending file per thread
def sendFile(arr_file, sock, dataId):
    dataArray = utility.fileSplitting(arr_file)
    for i in range(len(dataArray) - 1):
        sendPacket(dataArray[i], sock, dataId, i)
    sendPacket(dataArray[len(dataArray) - 1], sock, dataId, len(dataArray) - 1)

# Sending packet per thread
def sendPacket(data, sock, dataId, dataSequence):
    # Setting data length
    dataLength = utility.lengthCount(data)
    


    # Setting checksum
    sock.sendto(data.encode(), (UDP_IP, UDP_PORT))


# Configuring IP address and port
hostname = socket.gethostname()
UDP_IP = input("Insert target IP address:")
UDP_PORT = int(input("Insert target port: "))

print("UDP target IP:", UDP_IP)
print("UDP target port: ", UDP_PORT)

# Creating array of files that want to be transfered
files_num = int(input("Insert the number of files: "))
while files_num <= 0 or files_num > 5:
    print("Invalid amount of files")
    files_num = int(input("Insert the number of files: "))

arr_files = []
for i in range(files_num):
    selected_file = input("Insert file target relative to", os.path.dirname(os.path.abspath(__file__)))
    arr_files.append(selected_file)

# Connecting to socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for i in range(arr_files):
    socketThread = threading.Thread(target = "sendFile", args = (arr_files[i], sock, i))
    socketThread.start()

