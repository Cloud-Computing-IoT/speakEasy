import os
import sys
import TCP as tcp

# IP = "192.168.86.26"
DEVICES_LISTEN_PORT = 5006
RPI_LISTEN_PORT = 5005
BUFFER_SIZE = 1024
FILE_PATH = "/Users/matthewpisini/Desktop/testfile.mp3"

# sock = tcp.TCPsocket()
# connection = sock.listen(tcp.socket.gethostname(),LISTEN_PORT)

# sock = tcp.TCPserver()
# sock.listen(tcp.socket.gethostname(),DEVICES_LISTEN_PORT)

rpi_socket = tcp.TCPsocket()
rpi_socket.listen(tcp.socket.gethostname(),RPI_LISTEN_PORT)
rpi_socket.sendMessage("hello")
message = rpi_socket.receiveMessage()
print(message)
# sock.sendMessage("What you need?")
# sock.receiveFile(FILE_PATH)
# message = input("What do you want to send: ")
# sock.sendMessage(message)
# while True:
#     message = input("What do you want to send: ")
#     sock.sendMessage(message)
#     if message == "file":
#         sock.receiveFile("/Users/matthewpisini/Desktop/dummy.txt")
#     else:
#         data = sock.receiveMessage()
#         print(data)
#         if "Terminating" in data:
#             sock.closeSocket()
#             print("Finished listening")
#             sys.exit(1)
    
