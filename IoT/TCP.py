import os
import socket

BUFFER_SIZE = 1024
FILE_READ_SIZE = 1024



class TCPsocket:
    def __init__(self, TCP_IP, TCP_PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((TCP_IP,TCP_PORT))

    def sendMessage(self, message):
        self.s.send(message.encode())

    def sendFile(self, path):
        f = open(path, 'rb')
        l = f.read(FILE_READ_SIZE)
        while(l):
            self.s.send(l)
            l = f.read(FILE_READ_SIZE)
        f.close()

    def receive(self):
        data = self.s.recv(BUFFER_SIZE)
        return data.decode()

    def closeSocket(self):
        self.s.close()
