"""
Author: Matt Pisini 
Date: 12/8/20

Description:
Runs the 

Inputs (via CLI):

"""
import os
import time
import sys
import pexpect
import TCP as tcp
import threading
import ctypes
from queue import Queue

"""
arrow-up:      ^[[A
arrow-down:    ^[[B
arrow-right:   ^[[C
arrow-left:    ^[[D
"""
HOME_DIREC = "/home/pi/"

""" ******************** TCP GLOBALS ******************** """
TCP_IP = "192.168.86.26"
AWS_IP = "54.187.194.13"
AWS_COMMAND_PORT = 5005
AWS_FILE_PORT = 5006
LOST_CONNECTION_FLAG = 0
""" ************************v**************************** """

""" ******************** SONG GLOBALS ******************** """
MUSIC_PATH = "/home/pi/{music}"
SONG0 = "mp3_test.mp3"
SONG1 = "Lite_Weight.mp3"
SONG2 = "24kGoldn.mp3"
SONG_LIST = [SONG0, SONG1, SONG2]
SONG_NUM = 0
""" ******************************************************* """

""" ******************** RECORDING GLOBALS ******************** """
RECORD_COMMAND = "arecord -D hw:1,0 -d {time} -f cd {file_path}{file}.wav"
RECORD_COMMAND2 = "arecord -D hw:1,0 -f cd tester.wav"
FILE_LIMIT = 5
FINISHED_RECORDING = 1
RECORDING_LENGTH = 2
REC_COUNT = 0
RECORD_QUEUE = Queue()
""" *********************************************************** """

""" ******************** MUSIC/COMMAND GLOBALS ******************** """
OMXPLAYER_START = "delay: 0\r\n"
VOLUME_UP = '='
VOLUME_DOWN = '-'
PAUSE = ' '
NEXT = "next"
STOP = "stop"
COMMANDS = [VOLUME_DOWN, VOLUME_UP, PAUSE, NEXT, STOP]
COMMAND_QUEUE = Queue()
""" *************************************************************** """

ACCEL_DATA = '{  "linear_acceleration": {    "values": [      0.00235903263092041,      0.002854257822036743,      1.02996826171875E-4    ]  }}'

# This spawns a process to manage playing music to the speaker.
# Commands can be sent via the CLI to adjust control of the speaker.
class MusicChild:
	def __init__(self, sample_music):
		self.child = pexpect.spawn('omxplayer --vol -1800 ' + MUSIC_PATH.format(music = sample_music))
		self.child.expect(OMXPLAYER_START)

	def changeMusicOutput(self, command):
		self.child.send(command)
		if command == " ":
			output = None
		else: 
			self.child.expect("\r\n")
			output = self.child.before.decode()
		return output

	def terminateProcess(self):
		self.child.close()

# This class spawns a process to record for 'record_time' and save to 'file_name' path.
# The recording's 'file_name' is added to a global queue for transmission to AWS.
# The process will automatically terminate upon finishing recording.
class RecordChild:
	def __init__(self, record_time, file_name):
		global FINISHED_RECORDING
		print("starting recording")
		self.child = pexpect.spawn(RECORD_COMMAND.format(time = record_time, file_path = HOME_DIREC, file = file_name))
		self.child.expect(pexpect.EOF)
		global REC_COUNT, RECORD_QUEUE
		print("finished recording {}".format(REC_COUNT))
		RECORD_QUEUE.put("{}{}.wav".format(HOME_DIREC,file_name))
		REC_COUNT += 1
		if REC_COUNT >= FILE_LIMIT:
			cleanUpRecordings(REC_COUNT-FILE_LIMIT)
		FINISHED_RECORDING = 1

# Function deletes all recordings except for the last FILE_LIMIT
# recordings in home directory.
def cleanUpRecordings(current_num):
	for file in os.listdir(HOME_DIREC):
		if "rec{}".format(current_num) in file:
			os.remove(os.path.join(HOME_DIREC, file))

# This function
def controlInterface():
	try:
		AWS_socket = tcp.TCPsocket()
		AWS_socket.connect(AWS_IP, AWS_COMMAND_PORT)
		while True:
			message = AWS_socket.receiveMessage()
			if message.lower() == "file":
				AWS_socket.sendFile(RECORD_QUEUE.get())
			elif message in COMMANDS:
				# AWS_socket.sendMessage("Received: " + message)
				COMMAND_QUEUE.put(message)
				if message.lower() == "stop":
					AWS_socket.closeSocket()
					break
			else:
				AWS_socket.sendMessage("Invalid command: " + message)
	except:
		print("Lost connection to AWS")
		LOST_CONNECTION_FLAG = 1
		

def startMusic(song_num):
	global SONG_NUM
	music_child = MusicChild(SONG_LIST[SONG_NUM])
	print("Starting music with song: {}".format(SONG_LIST[SONG_NUM]))
	SONG_NUM += 1
	if SONG_NUM >= len(SONG_LIST):
		SONG_NUM = 0
	return music_child
		
def sendRecording(file_path):
	AWS_socket = tcp.TCPsocket()
	AWS_socket.connect(AWS_IP, AWS_FILE_PORT)
	try:
		AWS_socket.sendFile(file_path)
	except:
		print("Error sending file: " + file_path)

if __name__ == '__main__':
	music_child = startMusic(SONG_NUM)

	# command_lock = threading.Lock()
	# record_lock = threading.Lock()
	command_thread = threading.Thread(target=controlInterface, args=())
	command_thread.start()


	while True:
		if not music_child.child.isalive():
			print("Song is over... :(")
			music_child = startMusic(SONG_NUM)
		
		if not COMMAND_QUEUE.empty():
			message = COMMAND_QUEUE.get()
			if message.lower() == "stop":
				music_child.terminateProcess()
				command_thread.join()
				print("Shutting down execution...")
				sys.exit(1)
			elif message.lower() == "next":
				music_child.terminateProcess()
				music_child = startMusic(SONG_NUM)
			elif message == "=" or "-" or " ":
				output = music_child.changeMusicOutput(message)
				print(output)

		if FINISHED_RECORDING == 1:
			#create thread which will handle the recording subprocess
			FINISHED_RECORDING = 0
			x = threading.Thread(target=RecordChild, args=(RECORDING_LENGTH,"rec{}".format(REC_COUNT)))
			x.start()

		if not RECORD_QUEUE.empty():
			#create thread which will send recording
			x = threading.Thread(target=sendRecording, args=(RECORD_QUEUE.get(),))
			x.start()
		
		# Attempt to restablish connection with the AWS instance
		if LOST_CONNECTION_FLAG:
			LOST_CONNECTION_FLAG = 0
			command_thread = threading.Thread(target=controlInterface, args=())
			command_thread.start()