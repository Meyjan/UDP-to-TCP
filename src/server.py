import socket
import sys
import time
import threading
import logging

import utility

# Process that a thread should do once receiving a data from outside
def socketListening(packet, addr):
    # Socket listenting 
    print("Socket listening addr", addr)
    end = False

    # Getting packet and address of sender
    UDP_IP = addr[0]
    UDP_PORT = addr[1]
    nextPacket = packet

    dataId = utility.getPacketID(packet)
    newSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    newSock.bind((UDP_IP, (UDP_PORT + 1)))
    newSock.settimeout(5)

    print("Created port on:", (UDP_PORT + 1))
    
    nextAddr = addr

    print(utility.getPacketType(nextPacket))
    copiedFile = bytearray()

    if utility.getPacketType(nextPacket) == 0:

        while not end:
            print("Data Received. id = ", utility.getPacketID(nextPacket), "sequence = ", utility.getPacketSequenceNumber(nextPacket))

            checksum = utility.getChecksum(nextPacket)
            print("Checksum: ",checksum)
            packetArray = bytearray(nextPacket)
            packetArray[5] = 0x00
            packetArray[6] = 0x00

            # Sending ACK if file truly get
            if(utility.countCheckSum(packetArray) == checksum):
                print("Checksum correct")
                newSock.sendto(bytes(utility.returnACK(nextPacket)), nextAddr)
                copiedFile += utility.getData(nextPacket)
            else:
                print("Count checksum = ",utility.countCheckSum(packetArray))
                print("Checksum incorrect")

            nextPacket, _ = newSock.recvfrom(utility.MAX_PACKET_SIZE)
            if (utility.getPacketType(nextPacket) == 2):
                end = True
    
    end = False
    while not end:
        print("Data Received. id = ", utility.getPacketID(nextPacket), "sequence = ", utility.getPacketSequenceNumber(nextPacket))

        checksum = utility.getChecksum(nextPacket)
        print("Checksum: ",checksum)
        packetArray = bytearray(nextPacket)
        packetArray[5] = 0x00
        packetArray[6] = 0x00

        # Sending ACK if file truly get
        if(utility.countCheckSum(packetArray) == checksum):
            print("Checksum correct")
            copiedFile += utility.getData(nextPacket)
            end = True
        else:
            print("Count checksum = ",utility.countCheckSum(packetArray))
            print("Checksum incorrect")

    # Kirim FIN-ACK ke sender
    finale = utility.returnACK(nextPacket)
    print("Finale address: ", nextAddr)
    print("File type: ", utility.getPacketType(finale))
    newSock.sendto(bytes(finale),nextAddr)
    file = open('received/received.pdf','wb+')
    file.write(bytes(copiedFile))
    file.close()
            
    return 0

#----------------------------------------------------------------------------------------------------------------#
# Main program

UDP_IP = "192.168.43.184"
print("Socket Configured, IP = ", UDP_IP)
UDP_PORT = int(input("Masukkan port:"))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Binding socket
try:
    sock.bind((UDP_IP, UDP_PORT))
except socket.error as msg:
    print("Socket binding failed")
    sys.exit()
print("Socket Bound at", UDP_PORT)

# Create server log
log = logging.getLogger("server").setLevel(logging.DEBUG)

# Running a server
while True:
    try:
        print("Called")
        data, addr = sock.recvfrom(utility.MAX_PACKET_SIZE)
        print("Received from ", addr)
        socketThread = threading.Thread(target=socketListening, args=(data, addr))
        socketThread.start()
    
    except socket.error as msg:
        print("Socket threading failed")
        sys.exit()
        sock.close()