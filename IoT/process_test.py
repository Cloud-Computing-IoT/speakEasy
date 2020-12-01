import os
import socket

TCP_IP = "192.168.86.26"
TCP_PORT = 5005
BUFFER = 1024
MESSAGE = "Hello, world!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))
s.send(MESSAGE.encode())
data = s.recv(BUFFER.decode())
s.close()

print("DATA: " + data)