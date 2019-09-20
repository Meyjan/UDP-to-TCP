import socket

hostname = socket.gethostname()
UDP_IP = socket.gethostbyname(hostname)
UDP_PORT = int(input("Insert target port: "))
MESSAGE = "Hello, World Madahfakah!"

print("UDP target IP:", UDP_IP)
print("UDP target port: ", UDP_PORT)
print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))