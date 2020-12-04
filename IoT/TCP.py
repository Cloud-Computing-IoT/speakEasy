import os
import sys
import socket

BUFFER_SIZE = 1024
FILE_READ_SIZE = 1024



class TCPserver:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.child_sock = None #stores child socket forked once accepted

    def listen(self, TCP_IP, TCP_PORT):
        try:
            self.s.bind((TCP_IP, TCP_PORT))
            self.s.listen(1)
        except OSError as msg:
            print(msg)
            self.s.close()
            sys.exit(1)
        conn, addr = self.s.accept()
        self.child_sock = conn
        print("Received connection from: " + str(addr))

    def sendMessage(self, message):
        self.child_sock.send(message.encode())

    def sendFile(self, path):
        f = open(path, 'rb')
        l = f.read(FILE_READ_SIZE)
        while(l):
            self.child_sock.send(l)
            l = f.read(FILE_READ_SIZE)
        f.close()

    def receiveMessage(self):
        try:
            data = self.child_sock.recv(BUFFER_SIZE)
        except:
            print("Error: no child sock to receive")
        return data.decode()

    def receiveFile(self, filePath):
        try:
            f = open(filePath, 'wb')
        except:
            print("error opening file for writing: " + filePath)
        data = self.child_sock.recv(BUFFER_SIZE)
        while(data):
            f.write(data)
            data = self.child_sock.recv(BUFFER_SIZE)
        f.close()
        print("Finished receiving file " + filePath)

    def closeSocket(self):
        self.s.close()



class TCPsocket:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self, TCP_IP, TCP_PORT):
        try:
            self.s.connect((TCP_IP,TCP_PORT))
            print("Connected to " + TCP_IP)
        except:
            print("error connection to socket.")

    def sendMessage(self, message):
        self.s.send(message.encode())

    def sendFile(self, path):
        f = open(path, 'rb')
        l = f.read(FILE_READ_SIZE)
        while(l):
            self.s.send(l)
            l = f.read(FILE_READ_SIZE)
        f.close()
        print("Finished sending file " + path)

    def receiveMessage(self):
        data = self.s.recv(BUFFER_SIZE)
        return data.decode()

    def receiveFile(self, filePath):
        try:
            f = open(filePath, 'wb')
        except:
            print("error opening file for writing: " + filePath)
        data = self.s.recv(BUFFER_SIZE)
        while(data):
            f.write(data)
            data = self.s.recv(BUFFER_SIZE)

    def closeSocket(self):
        self.s.close()
