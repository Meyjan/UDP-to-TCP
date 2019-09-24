import socket
import os
import threading
import time

import utility

TYPE_DATA = 0x0
TYPE_ACK = 0x1
TYPE_FIN = 0x2
TYPE_FIN_ACK = 0x3


# Sending file per thread
def sendFile(arr_file, udp_ip, udp_port, dataId, sock):
    print("sendFile: called")

    dataArray = utility.fileSplitting(arr_file)

    if (len(dataArray) == 1):
        sendPacket(arr_file[0], sock, dataId, 0, TYPE_FIN)
    else:
        sendPacket(arr_file[0], sock, dataId, 0, TYPE_DATA)
    
    new_port = udp_port + 2*dataId + 1
    print(new_port)
    newSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    newSock.bind((udp_ip, new_port))
    newSock.settimeout(5)

    targetPort = socket.socket(socket.AF_INET, socket.S)
    for i in range(1, len(dataArray) - 1):
        sendPacket(dataArray[i], newSock, dataId, i, TYPE_DATA)
    sendPacket(dataArray[len(dataArray) - 1], newSock, dataId, len(dataArray) - 1, TYPE_FIN)


# Sending packet per thread
def sendPacket(data, sock, dataId, dataSequence, dataType):
    packet = utility.createPacketWithoutCheckSum(dataType, dataId, dataSequence, data)
    checksum = utility.countCheckSum(packet)
    print("count Checksum : ",checksum)
    utility.createPacketWithChecksum(packet, checksum)
    print("getChecksum : ",utility.getChecksum(packet))
    # Run sending files
    for i in range(10):
        print("Try", i)
        sock.sendto(bytes(packet), (UDP_IP, UDP_PORT))
        message = 0xFF
        message, addr = sock.recvfrom(utility.MAX_PACKET_SIZE)
        
        if message != 0xFF:
            if utility.getPacketType(message) == TYPE_ACK:
                break
            else:
                print("Packet id:", dataId, "sequence: ", dataSequence, "not acknowledged")
        else:
            print("Packet id:", dataId, "sequence: ", dataSequence, "not received")
    
    print("Packet id:", dataId, "sequence: ", dataSequence, "sent")


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
    selected_file = input("Insert file target relative to this file : ")
    arr_files.append(selected_file)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((UDP_IP, UDP_PORT))
print("Socket Bounded")

# Connecting to socket
for i in range(len(arr_files)):
    socketThread = threading.Thread(target = sendFile, args = (arr_files[i], UDP_IP, UDP_PORT, i, sock))
    socketThread.start()
