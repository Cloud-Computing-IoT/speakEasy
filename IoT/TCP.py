import os
import sys
import socket
import threading

BUFFER_SIZE = 1024
FILE_READ_SIZE = 1024
NUM_CONN = 5


"""
class TCPserver:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.child_sock = None #stores child socket forked once accepted

    def listen(self, TCP_IP, TCP_PORT):
        try:
            self.s.bind((TCP_IP, TCP_PORT))
            self.s.listen(NUM_CONN)
        except OSError as msg:
            print(msg)
            self.s.close()
            sys.exit(1)
        while True:
            conn, addr = self.s.accept()
            threading.Thread(target=self.processConnection, args=(conn,))
            print("Received connection from: " + str(addr))
        self.s.close()

    def processConnection(self, client_socket):
        message = self.receiveMessage(client_socket)
        return message
        
    def receiveMessage(self, socket):
        try:
            data = socket.recv(BUFFER_SIZE)
        except:
            print("Error: no child sock to receive")
        return data.decode()

    def receiveFile(self, filePath, socket):
        try:
            f = open(filePath, 'wb')
        except:
            print("error opening file for writing: " + filePath)
        data = socket.recv(BUFFER_SIZE)
        while(data):
            f.write(data)
            if len(data) < BUFFER_SIZE:
                break
            data = socket.recv(BUFFER_SIZE)
        f.close()
        print("Finished receiving file " + filePath)

    def closeSocket(self):
        self.s.close()
"""

class TCPsocket:
    #class is designed to set up single socket connections. By using listen, the object can wait for a single connection
    #on a specified port and store that socket as "child_socket". Any subsequent calls from that object will use this 
    #socket fd. This class can also be used to initiate the connection for a single TCP socket.
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.child_socket = None

    def connect(self, TCP_IP, TCP_PORT):
        try:
            self.s.connect((TCP_IP,TCP_PORT))
            print("Connected to " + TCP_IP)
        except:
            print("error connection to socket.")

    def listen(self, TCP_IP, TCP_PORT):
        try:
            self.s.bind((TCP_IP, TCP_PORT))
            self.s.listen(1)
        except OSError as msg:
            print(msg)
            self.s.close()
            sys.exit(1)
        conn, addr = self.s.accept()
        self.child_socket = conn
        print("Received connection from: " + str(addr))
        self.s.close()

    def sendMessage(self, message):
        if self.child_socket is not None:
            self.child_socket.send(message.encode())
        else:
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
        if self.child_socket is not None:
            data = self.child_socket.recv(BUFFER_SIZE)
        else:
            data = self.s.recv(BUFFER_SIZE)
        return data.decode()

    def receiveFile(self, filePath):
        try:
            f = open(filePath, 'wb')
        except:
            print("error opening file for writing: " + filePath)
        if self.child_socket is not None:
            socket = self.child_socket
        else:
            socket = self.s
        data = socket.recv(BUFFER_SIZE)
        while(data):
            f.write(data)
            if len(data) < BUFFER_SIZE:
                break
            data = socket.recv(BUFFER_SIZE)
        f.close()

    def closeSocket(self):
        if self.child_socket is not None:
            self.child_socket.close()
        else:
            self.s.close()
