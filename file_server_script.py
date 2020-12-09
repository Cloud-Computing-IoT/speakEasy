# Controller script for speaker

import sys
import socket
import threading

NUM_CONN = 5
BUFFER_SIZE = 1024
FILE_NUM = 0

def processFile(socket, addr, filePath):
    try:
        f = open(filePath, 'wb')
    except:
        print("error opening file for writing: " + filePath)
    data = socket.recv(BUFFER_SIZE)
    while(data):
        f.write(data)
        data = socket.recv(BUFFER_SIZE)
    f.close()


def TCPserver(TCP_IP, TCP_PORT):
    global FILE_NUM
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
        child = threading.Thread(target=processFile, args=(conn,addr,"{}{}.wav".format(FILE_PATH,FILE_NUM),)) 
        FILE_NUM += 1
        child.start()
        print("Received connection from: " + str(addr[0]))
    s.close()

if __name__ == "__main__":
    inputs = sys.argv
    LISTENING_PORT = inputs[1]
    FILE_PATH = inputs[2]
    TCPserver("0.0.0.0",LISTENING_PORT)
