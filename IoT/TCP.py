import os
import socket

# TCP_IP = "192.168.86.26"
# TCP_PORT = 5005
BUFFER_SIZE = 1024



class TCPsocket:
    def __init__(self, TCP_IP, TCP_PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((TCP_IP,TCP_PORT))

    def sendData(self, message):
        self.s.send(message.encode())

    def receive(self):
        data = self.s.recv(BUFFER_SIZE)
        return data.decode()

    def closeSocket(self):
        self.s.close()
