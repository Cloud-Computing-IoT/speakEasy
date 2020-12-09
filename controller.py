# Controller script for speaker

# from audio_analyzer import analyze_audio
from IoT import TCP as tcp
import sys
import socket
import threading
from multiprocessing import Process
from queue import Queue
import json

SERVER_MESSAGE_Q = Queue()
DEVICES_LISTEN_PORT = 5006
NUM_CONN = 5
BUFFER_SIZE = 1024

def parseObject(message, addr):
    new_message = json.loads(message)
    nums = {}
    nums[str(addr[0])] = new_message["linear_acceleration"]["values"] #list of 3 accel values 
    print(nums)
    SERVER_MESSAGE_Q.put(nums)

def processConnection(socket, addr):
    try:
        data = socket.recv(BUFFER_SIZE)
    except:
        print("Error: message not received")
    parseObject(data, addr)

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
        child.start()
        print("Received connection from: " + str(addr[0]))
    s.close()

if __name__ == "__main__":
    server_thread = threading.Thread(target=TCPserver, args=("0.0.0.0",DEVICES_LISTEN_PORT,))
    server_thread.start()
    # rpi_socket = tcp.TCPsocket()
    # rpi_socket.listen("0.0.0.0", RPI_LISTEN_PORT)
    # file_count = 0
    # while True:
    #     message = input("What do you want to send: ")
    #     rpi_socket.sendMessage(message)
    #     if message == "file":
    #         rpi_socket.receiveFile("/home/ubuntu/EE542_final_project/{}.wav".format(file_count))
    #         file_count += 1
    #     elif message == "stop":
    #         rpi_socket.closeSocket()
    #         sys.exit(1)
    #     else:
    #         data = rpi_socket.receiveMessage()
    #         print(data)
    #         if "Terminating" in data:
    #             rpi_socket.closeSocket()
    #             print("Finished listening")
    #             sys.exit(1)

    """
    while(True):
        # Retrieve data from mic and accelerometers

        input_audio_file = 'Another_day_w_voice_close.wav'

        # Analyze audio to determine which sound classes it contains
        results = analyze_audio.run(input_audio_file)

        # Process audio class results to adjust volume
        # Relevant classes:
        #   0: speech, 4: conversation, 16: laughter, 66: cheering, 137: music, 138: musical instrument
        volume_adjustment_audio = 0
        if(results[0] > .3):
            print("speech detected")
            volume_adjustment_audio = -1
        if results[66] > .1 or results[16] > .1:
            print("cheering or laughter detected")
            volume_adjustment_audio = 1

        # Process accelerometer data to adjust volume
        volume_adjustment_accelerometer = 0

        
        # Adjust volume
        volume += volume_adjustment_audio
        volume += volume_adjustment_accelerometer
        if(volume < 1):
            volume = 1
        elif(volume > 10):
            volume = 10

        # Send command to speaker to adjust volume
        print(volume)
"""