import socket
import sys
import time
import threading
import logging

import utility

port_pool = [5001, 5002, 5003, 5004, 5005, 5006, 5007, 5008, 5009, 5010, 5011, 5012, 5013, 5014, 5015, 5016, 5017, 5018, 5019, 5020]

# Process that a thread should do once receiving a data from outside
def socketListening(packet, addr):
    # Socket listenting 
    print("Socket listening addr", addr)
    end = False

    # Getting packet and address of sender
    UDP_IP = addr[0]
    UDP_PORT = addr[1]
    nextPacket = packet

    newSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    newSock.settimeout(5)

    # try:
    dataId = utility.getPacketID(packet)

    readyPort = 0

    print(port_pool)
    print(port_pool[0])

    # Looking for port to bind
    if (not port_pool):
        print("Cannot bind socket")
    else:
        readyPort = port_pool.pop(0)
        newSock.bind((UDP_IP, readyPort))
        print("Created port on:", readyPort)

    nextAddr = addr

    # Processing file name
    fileName = utility.getData(packet)
    print("File name = ", fileName)

    checksum = utility.getChecksum(nextPacket)
    packetArray = bytearray(nextPacket)
    packetArray[5] = 0x00
    packetArray[6] = 0x00

    # Sending ACK and agreed port
    clientPort = (readyPort).to_bytes(2, byteorder='big')
    packet = utility.createPacketWithoutCheckSum(0x01, dataId, 0, clientPort)
    if(utility.countCheckSum(packetArray) == checksum):
        print("Sending packet to:", nextAddr)              
        newSock.sendto(bytes(packet), nextAddr)       
        print("Package return sent")     
    else:
        print("Count checksum = ",utility.countCheckSum(packetArray))
        print("Checksum incorrect")

    nextPacket, nextAddr = newSock.recvfrom(utility.MAX_PACKET_SIZE)
    if (utility.getPacketType(nextPacket) == 2):
        end = True


    copiedFile = bytearray()

    if utility.getPacketType(nextPacket) == 0:

        while not end:
            print("Data Received. id = ", utility.getPacketID(nextPacket), "sequence = ", utility.getPacketSequenceNumber(nextPacket))

            checksum = utility.getChecksum(nextPacket)
            packetArray = bytearray(nextPacket)
            packetArray[5] = 0x00
            packetArray[6] = 0x00

            # Sending ACK if file truly get
            if(utility.countCheckSum(packetArray) == checksum):                
                newSock.sendto(bytes(utility.returnACK(nextPacket)), nextAddr)              
                copiedFile += utility.getData(nextPacket)
                
            else:
                print("Count checksum = ",utility.countCheckSum(packetArray))
                print("Checksum incorrect")

            nextPacket, nextAddr = newSock.recvfrom(utility.MAX_PACKET_SIZE)
            if (utility.getPacketType(nextPacket) == 2):
                end = True

    end = False
    while not end:
        print("Data Received. id = ", utility.getPacketID(nextPacket), "sequence = ", utility.getPacketSequenceNumber(nextPacket))

        checksum = utility.getChecksum(nextPacket)
        packetArray = bytearray(nextPacket)
        packetArray[5] = 0x00
        packetArray[6] = 0x00

        # Sending ACK if file truly get
        if(utility.countCheckSum(packetArray) == checksum):
            copiedFile += utility.getData(nextPacket)
            end = True
        else:
            print("Count checksum = ",utility.countCheckSum(packetArray))
            print("Checksum incorrect")

    # Kirim FIN-ACK ke sender
    finale = utility.returnACK(nextPacket)
    newSock.sendto(bytes(finale),nextAddr)

    print(fileName)
    fileName = "received/" + fileName.decode("utf-8")
    file = open(fileName,'wb')
    file.write(bytes(copiedFile))
    file.close()

    if readyPort == 0:
        port_pool.append(readyPort)
        
    # except:
    #     print("Error. Can't listen to the packet")

    # finally:
    #     print()
    #     newSock.close()
            
    return 0

#----------------------------------------------------------------------------------------------------------------#
# Main program

UDP_IP = "192.168.43.33"
print("Socket Configured, IP = ", UDP_IP)
UDP_PORT = int(input("Masukkan port:"))

# Binding socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# try:
sock.bind((UDP_IP, UDP_PORT))
# except socket.error as msg:
#     print("Socket binding failed")
#     sys.exit()
print("Socket Bound at", UDP_PORT)

# Create server log
log = logging.getLogger("server").setLevel(logging.DEBUG)

# Empty socket
emptySocket = []

# Running a server
while True:
    try:
        print("Main socket is ready...")
        data, addr = sock.recvfrom(utility.MAX_PACKET_SIZE)
        socketThread = threading.Thread(target=socketListening, args=(data, addr))
        socketThread.start()
        time.sleep(1)
    
    except socket.error as msg:
        print("Socket threading failed")
        sys.exit()
        sock.close()