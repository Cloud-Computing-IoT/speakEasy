# Controller script for speaker

from audio_analyzer import analyze_audio
import TCP as tcp
import socket
import threading
from multiprocessing import Process
from queue import Queue
import json
import queue
import os
import math
from statistics import mean

def get_vector_mag(vector_input):
    #assuming m/s^2
    mag = sqrt(sum([x**2 for x in vector_input]))
    return mag - 9.8

def parseObject(message, addr):
    new_message = json.loads(message)
    nums = {}
    nums[str(addr[0])] = new_message["linear_acceleration"]["values"]  # list of 3 accel values
    SERVER_MESSAGE_Q.put(nums)


def processConnection(socket, addr):
    try:
        data = socket.recv(BUFFER_SIZE)
    except:
        print("Error: message not received")
    parseObject(data, addr)
    # SERVER_MESSAGE_Q.put(data.decode())


class CentralIO:
    def __init__(self, IP, audio_port, dance_port):
        self.IP = IP
        self.dance_port = dance_port
        self.danceDataQueue = queue.Queue()
        self.audioFileQueue = queue.Queue()
        self.commandQueue = queue.Queue()
        self.voiceConnection = TCPSocket()
        self.voiceConnection.connect(self.IP, self.audio_port)
        self.base_path = ""

    def danceServer(self):
        TCP_IP = self.IP
        TCP_PORT = self.dance_port
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
            child = threading.Thread(target=self.danceIO, args=(conn, addr,))
            # child = Process(target=processConnection, args=(conn,))
            child.start()
            print("Received connection from: " + str(addr[0]))
        s.close()
    def danceIO(self):
            try:
                data = socket.recv(BUFFER_SIZE)
            except:
                print("Error: message not received")
            parseObject(data, addr)
            # SERVER_MESSAGE_Q.put(data.decode())
            new_message = json.loads(data)
            nums = {}
            nums[str(addr[0])] = new_message["linear_acceleration"]["values"]  # list of 3 accel values
            self.danceDataQueue.put(nums)
    def audioIO(self):
        file_id = 0
        while True:
            #recieve file
            file_name = os.path.join(self.base_path, "%d.wav"%(file_id))
            self.audioConnection.recieveFile(file_name)
            file_id += 1
            self.audioFileQueue.put(file_name)
            #check for commands to send
            while not self.commandQueue.empty():
                self.voiceConnection.sendMessage(self.commandQueue.get())
        self.audioConnection.closeSocket()

class VolumeController:
    def __init__(self, starting_volume):
        self.proposed_volume = 5
        self.current_volume = 5
        self.bias_volume = 5
        self.threshold = 5

        self.raw_values = []
        self.raw_values_length = 100



        self.audioFeatures = {"speech": 0, "conversation": 4, "laughter": 16, "cheering" : 66,
                                "music": 137, "musical_insturment": 138}
        self.featureWeights = {"speech": -1, "conversation": -1, "laughter": +1, "cheering": +1,
                                "music": 0, "musical_insturment": 0, "dance": 1}
        self.audio_class_threshold = .1
        self.dance_threshold = 10

        # moving average filter if needed
        self.audio_buffer_length = 3
        self.audioBuffers = {param : [] for param in self.audioFeatures.keys()}

        #moving average accelerator buffer
        self.dance_buffer_length = 10
        self.danceBuffer = []
        self.danceStorage = {}
        self.dance_storage_ttl = 10



        #logistic curve
        self.x_not = 10
        self.scale = .5
        self.L = 1

    def audio_input(self, results):
        self.voiceBuffers
        for key, value in self.audioFeatures:
            self.audioBuffers[key].append(results[key])
            if len(self.audioBuffers[key]) > self.audio_buffer_length:
                self.audioBuffers[key] = self.audioBuffers[key][1:]
    def processDance(self, results):

        self.danceStorage = {}
        self.dance_storage_ttl = 10
        runsum = 0.0
        # not sure if well need this dance storage but just in case
        for person, value in results:
            mag = get_vector_mag(value)
            runsum += mag
            if person in self.danceStorage.keys():
                self.danceStorage[person]["TTL"] = self.dance_storage_ttl
                self.danceStorage[person]["Mag"].append(mag)
            else:
                self.danceStorage[person] = {"TTL": self.dance_storage_ttl, "Mag": mag}
        for entry in self.danceStorage:
            entry["TTL"] -= 1
        self.danceBuffer.append(runsum/len(results))
        if len(self.danceBuffer) > self.dance_buffer_length: 
            self.danceBuffer = self.danceBuffer[1:]
        return self.getVolumeChange()

    def processAudio(self):
        value = 0
        # conversation makes volume go up no matter what
        #audio_values = {param : (mean(self.audioBuffers[param]) > self.audio_class_threshold)
                        #for param in self.audioFeatures.keys()}
        values = {param : (mean(self.audioBuffers[param]) for param in self.audioFeatures.keys()}
        values["dance"] = mean(self.danceBuffer)
        new_value = sum([values[key]*self.featureWeights[key] for key in self.audioFeatures.keys()])
        self.raw_values.append(new_value)
        for old_value in self.raw_values[:-1]:
            if (abs(new_value - old_value) > self.threshold):
                self.current_volume += (new_value - old_value)*self.get_bias_function((new_value - old_value))
                return self.current_volume
        return self.getVolumeChange
    def getVolumeChange(self):
        delta = self.proposed_volume - self.current_volume
        self.proposed_volume = self.current_volume
        self.raw_values = self.raw_values[-1:] #dont need past values anymore
        return delta


    def _getBiasFunction(self, proposed_delta):

        #I use the derivative of logtistic function to bias (think guassian)
        # We bias towards volume 5
        #direction = 1: moving towards the mean, accelerate more the farther we are away
        #direction = 0 moving away from the mean, accelerate less the farther we get away
        direction =  ((proposed_delta * (self.bias_volume - self.current_volume)) > 0)

        x = (self.current_volume - self.x_not)*(-self.scale)
        denom = (math.exp(x) + 1)**2
        num = self.scale*self.L*x

        if direction:
            return 1 - (num/denom)
        else:
            return num/denom









if __name__ == "__main__":
    mainInterface = CentralIO()
    danceIOThread = threading.Thread(target = mainInterface.danceServer)
    danceIOThread.start()
    volumeControl = VolumeController()
    audioThread = threading.Thread(target = mainInterface.audioIO)
    volume = 5 # set this as the begining
    while (True):

        while not mainInterface.audioFileQueue.empty(): 
            input_audio_file = mainInterface.audioFileQueue.get()
            results = analyze_audio.run(input_audio_file)
            delta = volumeControl.processAudio(results)
            # check for volume change each time for low latency
            if delta:
                mainInterface.commandQueue.put(delta)

        while not mainInterface.danceDataQueue():
            delta = volumeControl.processDance(volumeControl.mainInterface.danceDataQueue.get())
            if delta:
                mainInterface.commandQueue.put(delta)

