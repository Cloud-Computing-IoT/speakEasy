import os
import socket

TCP_IP = "192.168.86.26"
TCP_PORT = 5005
BUFFER = 1024
MESSAGE = "Hello, world!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER)
s.close()

print("DATA: " + data)