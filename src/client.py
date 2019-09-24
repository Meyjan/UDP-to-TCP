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
def sendFile(arr_file, UDP_IP, UDP_PORT, dataId):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    new_port = UDP_PORT + 2 * dataId + 1
    sock.bind((UDP_IP, new_port))
    sock.settimeout(6)

    print("Created port on:", new_port)

    dataArray = utility.fileSplitting(arr_file)
    print(len(dataArray))

    if (len(dataArray) <= 1):
        sendPacket(dataArray[0], sock, dataId, 0, TYPE_FIN, (UDP_IP, UDP_PORT))
    else:
        sendPacket(dataArray[0], sock, dataId, 0, TYPE_DATA, (UDP_IP, UDP_PORT))
        target_port = UDP_PORT + 2 * dataId + 2
        for i in range(1, len(dataArray) - 1):
            sendPacket(dataArray[i], sock, dataId, i, TYPE_DATA, (UDP_IP, target_port))
        sendPacket(dataArray[len(dataArray) - 1], sock, dataId, len(dataArray) - 1, TYPE_FIN, target_port)


# Sending packet per thread
def sendPacket(data, sock, dataId, dataSequence, dataType, addr):
    # Packet creation
    packet = utility.createPacketWithoutCheckSum(dataType, dataId, dataSequence, data)
    checksum = utility.countCheckSum(packet)
    utility.createPacketWithChecksum(packet, checksum)

    # Run sending files
    for i in range(10):
        # Sending file procedure
        print("Packet type: ", utility.getPacketType(packet))
        sent_packet = bytes(packet)
        sock.sendto(bytes(packet), addr)
        message = 0xFF
        message, sender_addr = sock.recvfrom(utility.MAX_PACKET_SIZE)
        
        if message != 0xFF:
            if utility.getPacketType(message) == dataType + 1:
                break
            else:
                print("Packet id:", dataId, "sequence: ", dataSequence, "not acknowledged")
        else:
            print("Packet id:", dataId, "sequence: ", dataSequence, "not received")
    
    print("Packet id:", dataId, "; sequence:", dataSequence, "sent")


# Configuring IP address and port
hostname = socket.gethostname()
UDP_IP = input("Insert target IP address:")
UDP_PORT = int(input("Insert target port:"))

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

print()
print("Socket Bounded")

# Connecting to socket
for i in range(len(arr_files)):
    socketThread = threading.Thread(target = sendFile, args = (arr_files[i], UDP_IP, UDP_PORT, i))
    socketThread.start()
