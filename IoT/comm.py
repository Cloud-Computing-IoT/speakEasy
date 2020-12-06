import os
import sys
import TCP as tcp

# IP = "192.168.86.26"
LISTEN_PORT = 5005
BUFFER_SIZE = 1024
FILE_PATH = "/Users/matthewpisini/Desktop/testfile.mp3"

# sock = tcp.TCPsocket()
# connection = sock.listen(tcp.socket.gethostname(),LISTEN_PORT)

sock = tcp.TCPserver()
sock.listen(tcp.socket.gethostname(),LISTEN_PORT)

# sock.sendMessage("What you need?")
# sock.receiveFile(FILE_PATH)
message = input("What do you want to send: ")
sock.sendMessage(message)
while True:
    data = sock.receiveMessage()
    print(data)
    if "Terminating" in data:
        sock.closeSocket()
        print("Finished listening")
        sys.exit(1)
    message = input("What do you want to send: ")
    sock.sendMessage(message)
