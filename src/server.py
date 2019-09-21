import socket
import sys
import time
import threading
import logging

import utility

# Process that a thread should do once receiving a data from outside
def socketListening(data, addr):
    end = False
    nextData = data

    if utility.getDataType(data) == 0:
        while not end:
            result = utility.packageOpening(nextData)
            # Simpan data-data yang dibutuhkan di <sini>


            # Kirim ACK ke user. Lalu, terima paket dari user
            
            nextData, nextAddr = sock.recvfrom(65592)
            if (utility.getDataType(data) == 2):
                end = True

    # Responi data-data yang diberikan di <sini>
    
    # Kirim FIN-ACK ke sender
            
    return 0


# Configuring log
logging.basicConfig(level = logging.DEBUG)

# Configuring socket
hostname = socket.gethostname()
UDP_IP = socket.gethostbyname(hostname)
UDP_PORT = int(input("Insert target port: "))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Socket Configured")

# Binding socket
try:
    sock.bind((UDP_IP, UDP_PORT))
except socket.error as msg:
    print("Socket binding failed. Error code:", str(msg[0]), "; Message", msg[1])
    sys.exit()
print("Socket Bound")

# Create server log
log = logging.getLogger("server").setLevel(logging.DEBUG)


while True:
    try:
        data, addr = sock.recvfrom(65592)
        socketThread = threading.Thread(target=socketListening, args=(data, addr))
        socketThread.start()
    
    except socket.error as msg:
        print("Socket threading failed. Error code:", str(msg[0]), "; Message", msg[1])
        sys.exit()

sock.close()