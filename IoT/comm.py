import os
import sys
import TCP as tcp
import socket
import threading
from multiprocessing import Process
from queue import Queue
import json

# IP = "192.168.86.26"
DEVICES_LISTEN_PORT = 5006
RPI_LISTEN_PORT = 5005
BUFFER_SIZE = 1024
FILE_PATH = "/Users/matthewpisini/Desktop/testfile.mp3"
NUM_CONN = 5
SERVER_MESSAGE_Q = Queue()

def parseObject(message, addr):
    new_message = json.loads(message)
    nums = {}
    nums[str(addr[0])] = new_message["linear_acceleration"]["values"] #list of 3 accel values 
    SERVER_MESSAGE_Q.put(nums)

def processConnection(socket, addr):
    try:
        data = socket.recv(BUFFER_SIZE)
    except:
        print("Error: message not received")
    parseObject(data, addr)
    # SERVER_MESSAGE_Q.put(data.decode())

def TCPserver(TCP_IP, TCP_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((TCP_IP, TCP_PORT))
        s.listen(NUM_CONN)
    except OSError as msg:
        print(msg)
        s.close()
        sys.exit(1)
    while True:
        conn, addr = s.accept()
        child = threading.Thread(target=processConnection, args=(conn,addr,))
        # child = Process(target=processConnection, args=(conn,))
        child.start()
        print("Received connection from: " + str(addr[0]))
    s.close()

if __name__ == "__main__":
    print("making thread")
    server_thread = threading.Thread(target=TCPserver, args=(socket.gethostname(),DEVICES_LISTEN_PORT,))
    server_thread.start()
    print("made thread")

    while True:
        if not SERVER_MESSAGE_Q.empty():
            print(SERVER_MESSAGE_Q.get())
            # for item in dict(message):
            #     print(item)
            #     for elem in item:
            #         print(elem)
            
    """
    rpi_socket = tcp.TCPsocket()
    rpi_socket.listen(tcp.socket.gethostname(),RPI_LISTEN_PORT)

    while True:
        message = input("What do you want to send: ")
        rpi_socket.sendMessage(message)
        if message == "file":
            rpi_socket.receiveFile("/Users/matthewpisini/Desktop/dummy.txt")
        else:
            data = rpi_socket.receiveMessage()
            print(data)
            if "Terminating" in data:
                rpi_socket.closeSocket()
                print("Finished listening")
                sys.exit(1)
    """
