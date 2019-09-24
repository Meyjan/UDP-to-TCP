import socket
import sys
import time
import threading
import logging

import utility

# Process that a thread should do once receiving a data from outside
def socketListening(packet, addr, udp_ip, udp_port):
    print("Socket listening")
    end = False
    nextPacket = packet
    
    f = open('received/received.pdf','wb')

    dataId = utility.getPacketID(packet)
    nextAddr = (udp_ip, (udp_port + (2 * dataId) + 1))
    newSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    newSock.bind((udp_ip, (udp_port + (2 * dataId) + 2)))
    print(udp_port + (2 * dataId) + 2)

    if utility.getPacketType(nextPacket) == 0:
        while not end:
            # Simpan data-data yang dibutuhkan di <sini>
            print("data Received")

            checksum = utility.getChecksum(nextPacket)
            print("Checksum: ",checksum)
            packetArray = bytearray(nextPacket)
            packetArray[5] = 0x00
            packetArray[6] = 0x00
            if(utility.countCheckSum(packetArray) == checksum):
                # Kirim ACK ke user. Lalu, terima paket dari user
                print("Checksum correct")
                newSock.sendto(bytes(utility.returnACK(nextPacket)), nextAddr)
            else:
                print("Count checksum = ",utility.countCheckSum(packetArray))
                print("Checksum incorrect")

            nextPacket, _ = newSock.recvfrom(32775)
            if (utility.getPacketType(nextPacket) == 2):
                end = True

    # Responi data-data yang diberikan di <sini>
    print("Done bitcheese")
    
    # Kirim FIN-ACK ke sender
    newSock.sendto(bytes(utility.returnACK(nextPacket)),nextAddr)
            
    return 0

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
print("Socket Bound")

# Create server log
log = logging.getLogger("server").setLevel(logging.DEBUG)


while True:
    try:
        data, addr = sock.recvfrom(32775)
        socketThread = threading.Thread(target=socketListening, args=(data, addr, UDP_IP, UDP_PORT))
        socketThread.start()
    
    except socket.error as msg:
        print("Socket threading failed")
        sys.exit()
        sock.close()