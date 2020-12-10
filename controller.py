# Controller script for speaker
#hey whats up
from audio_analyzer import analyze_audio
import sys
sys.path.append("/home/ubuntu/EE542_final_project/Cloud-Enabled-Smart-Speaker/IoT")

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
import numpy as np
import random
from multiprocessing import Process
from contextlib import contextmanager
from subprocess import Popen, PIPE, STDOUT
from time import sleep, time
from matplotlib import pyplot as plt
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)


AUDIO_FILE_NAME = "input.wav"
RECORDINGS_DIRECTORY = "/home/ubuntu/EE542_final_project/recordings"
AUDIO_FILE_PATH = os.path.join(RECORDINGS_DIRECTORY, AUDIO_FILE_NAME)
FILE_SERVER_PORT = 5006
RUN_FILE_SERVER = 'python3 file_server_script.py {}'.format(FILE_SERVER_PORT)
VISUALIZER_PORT = 6969
IP = "0.0.0.0"


def get_vector_mag(vector_input):
    #assuming m/s^2
    mag = sqrt(sum([x**2 for x in vector_input]))
    return mag - 9.8



class CentralIO:
    def __init__(self, IP = "0.0.0.0", volume_port = 5005, dance_port=4204):
        self.IP = IP
        self.dance_port = dance_port
        self.volume_port = volume_port
        self.danceDataQueue = queue.Queue()
        self.audioFileQueue = queue.Queue()
        self.commandQueue = queue.Queue()
        self.audioConnection = tcp.TCPsocket()
        #get rid of this try block
        try:
            self.audioConnection.listen(self.IP, self.volume_port)
        except:
            print("WTFWTFWTF")
            pass


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
        while True:
            #check for commands to send
            while not self.commandQueue.empty():
                value = self.commandQueue.get()
                if value > 0:
                    message = '='
                else:
                    message = '-'
                self.audioConnection.sendMessage(message)

        self.audioConnection.closeSocket()

class VolumeController:
    def __init__(self, starting_volume = 5):
        self.proposed_volume = 5
        self.current_volume = 5
        self.bias_volume = 5
        self.threshold = .01

        self.raw_values = []
        self.raw_values_length = 100



        self.audioFeatures = {"speech": 0, "conversation": 4, "laughter": 16, "cheering" : 66,
                                "music": 137, "musical_insturment": 138}
        self.featureWeights = {"speech": -1, "conversation": -1, "laughter": +1, "cheering": +1,
                                "music": 0, "musical_insturment": 0, "dance": 1}


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


    def inputDance(self, results):

        self.danceStorage = {}
        self.dance_storage_ttl = 10
        runsum = 0.0
        # not sure if well need this dance storage but just in case
        for person, value in results.items():
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
        return self._process()

    def inputAudio(self, results):
        for key, value in self.audioFeatures.items():
            self.audioBuffers[key].append(results[value])
            if len(self.audioBuffers[key]) > self.audio_buffer_length:
                self.audioBuffers[key] = self.audioBuffers[key][1:]
        return self._process()

    def _process(self):
        print(self.audioBuffers)
        values = {key : (mean(value)) for key, value in self.audioBuffers.items()}
        for key, value in values.items():
            print(key, value)
        try:
            values["dance"] = mean(self.danceBuffer)
        except:
            #empty array rn
            values["dance"] = 0
        try:
            output_string = ""
            for key, value in values.items():
                output_string += " %s  %.4f "%(key, value)
            visualizer.sendMessage(output_string)
        except Exception as inst:
            print(type(inst))
            print(inst)
            pass
        new_value = sum([values[key]*self.featureWeights[key] for key in self.audioFeatures.keys()])
        self.raw_values.append(new_value)
        for old_value in (self.raw_values[:-1]):
            some_value = old_value
            if self.threshold < abs(new_value - some_value):
                self.proposed_volume += self.current_volume + self._getBiasFunction((new_value - old_value))
                return self._getVolumeChange()
        return 0
    def _getVolumeChange(self):
        delta = self.proposed_volume - self.current_volume
        self.proposed_volume = self.current_volume
        self.raw_values = self.raw_values[-1:] #dont need past values anymore
        print("New value of delta %f"%(delta))
        return delta

    def _getBiasFunction(self, proposed_delta):

        #I use the derivative of logtistic function to bias (think guassian)
        # We bias towards volume 5
        #direction = 1: moving towards the mean, accelerate more the farther we are away
        #direction = 0 moving away from the mean, accelerate less the farther we get away
        direction = abs(self.bias_volume - self.current_volume - proposed_delta) < abs(self.bias_volume - self.current_volume)

        x = math.exp((self.current_volume - self.x_not)*(-self.scale))
        denom = (x + 1)**2
        num = self.scale*self.L*x
        if direction:
            return max(min(1 - (num/denom), 1), 0)*proposed_delta
        else:
            return max(min(num/denom, 1), 0)*proposed_delta

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout



def runFileServer():

    a = Popen(RUN_FILE_SERVER, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)



    print("File Server Process Launched", a.pid)
    start = time()
    while a.poll() == None or time()-start <= 30: #30 sec grace period
        sleep(0.25)
    if a.poll() == None:
        print('Still running, killing')
        a.kill()
    else:
        print('exit code:',a.poll())
    output = a.stdout.read()
    a.stdout.close()
    a.stdin.close()
    return output



##########################################
#MAIN
##########################################

if __name__ == "__main__":
    begin_flag = 1
    audioStream = threading.Thread(target = runFileServer) # should this be processs or thread ?
    audioStream.start()
    visualizer = tcp.TCPsocket()
    visualizerThread = threading.Thread(target = visualizer.listen,
                                        args = [IP, VISUALIZER_PORT])
    visualizerThread.start()

    mainInterface = CentralIO()
    danceIOThread = threading.Thread(target = mainInterface.danceServer)
    #danceIOThread.start()
    volumeControl = VolumeController()
    audioIOThread = threading.Thread(target = mainInterface.audioIO)
    audioIOThread.start()
    volume = 5 # set this as the begining
    epoch = 0
    while (True):

        epoch += 1
        print("epoch = %d"%(epoch))
        for filename in os.listdir(RECORDINGS_DIRECTORY):
            if filename.endswith(".wav"):
                current_file = os.path.join(RECORDINGS_DIRECTORY, filename)
                #os.path.rename(current_file, AUDIO_FILE_PATH)
                with suppress_stdout():
                    results = analyze_audio.run(current_file, begin_flag)

                    begin_flag = 0
                print("current file is %s" % (current_file))
                #debug
                #results = {random.randint(1, 100) : val for val in volumeControl.audioFeatures.values()}
                temp = [results[val] for val in volumeControl.audioFeatures.values()]
                print(temp)

                delta = volumeControl.inputAudio(results)
                if delta:
                    mainInterface.commandQueue.put(delta)

                os.remove(current_file)


        while not mainInterface.danceDataQueue.empty():

            delta = volumeControl.processDance(volumeControl.mainInterface.danceDataQueue.get())
            if delta:
                mainInterface.commandQueue.put(delta)


    audioStream.join()
    #danceIOThread.join()
    audioIOThread.join()
    visualizerThread.join()
