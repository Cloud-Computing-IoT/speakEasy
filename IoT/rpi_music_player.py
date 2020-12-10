"""
Author: Matt Pisini 
Date: 12/8/20

Description:
This code runs on the RPi and handles several functionl:
1. Runs process for the speaker through OMXplayer CLI. We can send commands 
to this process in order to change volume, pause the music, or skip the song.
2. Runs process for recording audio clips with the attached microphone. These
recordings are of set length and are saved locally before sending to AWS.
3. Runs a process for communicating with AWS in order to receive speaker commands.
4. Runs processes to send the .wav recording files for every file created.

Inputs (via CLI):
None

"""

import os
import time
import sys
import pexpect
import TCP as tcp
import threading
from queue import Queue

HOME_DIREC = "/home/pi/"		#Path to RPi home directory

""" ******************** TCP GLOBALS ******************** """
AWS_IP = "54.187.194.13"		#IP address of AWS EC2 instance
AWS_COMMAND_PORT = 5005			#Port number for AWS controller
AWS_FILE_PORT = 5006			#Port number to send .wav files
LOST_CONNECTION_FLAG = 0		#Flag if conneection to AWS is lost
""" **************************************************** """

""" ******************** SONG GLOBALS ******************** """
MUSIC_PATH = "/home/pi/{music}"
SONG0 = "DPunk.mp3"
SONG1 = "Lite_Weight.mp3"
SONG2 = "24kGoldn.mp3"
SONG3 = "Ah_Bellaire.mp3"
SONG4 = "City_of_stars.mp3"
SONG5 = "Pure_Imagination.mp3"
SONG_LIST = [SONG0, SONG1, SONG2, SONG3, SONG4, SONG5]
SONG_NUM = 0
""" ******************************************************* """

""" ******************** RECORDING GLOBALS ******************** """
RECORD_COMMAND = "arecord -D hw:2,0 -d {time} -f cd {file_path}{file}.wav"
FILE_LIMIT = 5					#File limit local sttorage
FINISHED_RECORDING = 1			#Flag to start new recording
RECORDING_LENGTH = 2			#Recording duration in seconds
REC_COUNT = 0					#Current recording number
RECORD_QUEUE = Queue()			#Queue to store recording paths
""" *********************************************************** """

""" ******************** MUSIC/COMMAND GLOBALS ******************** """
OMXPLAYER_START = "delay: 0\r\n" #expected output when invoking OMXplayer
VOLUME_UP = '='
VOLUME_DOWN = '-'
PAUSE = ' '
NEXT = 'next'
STOP = 'stop'
FAST_FORWARD = '^[[C'
REWIND = '^[[D'
COMMANDS = [VOLUME_DOWN, VOLUME_UP, PAUSE, NEXT, STOP, FAST_FORWARD, REWIND]
COMMAND_QUEUE = Queue()
""" *************************************************************** """


ACCEL_DATA = '{  "linear_acceleration": {    "values": [      0.00235903263092041,      0.002854257822036743,      1.02996826171875E-4    ]  }}'

# This class spawns a process to manage playing music to the speaker.
# Commands can be sent via the CLI to adjust control of the speaker.
class MusicChild:
	def __init__(self, sample_music):
		# We start at volume 12 (-18dB) range is [-51dB, 6dB] (20 increments)
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

# This function maintains communication with AWS in order to receive commands.
# All received input is added to a global queue for processing in the main loop.
def controlInterface():
	try:
		AWS_socket = tcp.TCPsocket()
		AWS_socket.connect(AWS_IP, AWS_COMMAND_PORT)
		print("Connected to AWS control interface on port " + str(AWS_COMMAND_PORT))
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
		print("Lost connection to AWS control interface")
		global LOST_CONNECTION_FLAG
		LOST_CONNECTION_FLAG = 1
		
# Function called in main loop to invokes speaker process for playing a song.
# Returns the created MusicChild object.
def startMusic(song_num):
	global SONG_NUM
	music_child = MusicChild(SONG_LIST[SONG_NUM])
	print("Starting music with song: {}".format(SONG_LIST[SONG_NUM]))
	SONG_NUM += 1
	if SONG_NUM >= len(SONG_LIST):
		SONG_NUM = 0
	return music_child

# This function is called by a thread created to send a recording file to AWS.
def sendRecording(file_path):
	AWS_socket = tcp.TCPsocket()
	AWS_socket.connect(AWS_IP, AWS_FILE_PORT)
	try:
		AWS_socket.sendFile(file_path)
		os.remove(file_path)
	except:
		print("Error sending file: " + file_path)
		pass

if __name__ == '__main__':

	# Spawn initial music playing process
	music_child = startMusic(SONG_NUM)
	# Spawn communication thread with AWS for commands.
	command_thread = threading.Thread(target=controlInterface, args=())
	command_thread.start()

	MIN_VOLUME_REACHED = 0
	MAX_VOLUME_REACHED = 0
	# Main loop: handles speaker control, spawning speaker processes, 
	# recording processes, sending recordings, and connection restablishment.
	while True:
		# Check if the music playing process is alive. If not, start a new one.
		if not music_child.child.isalive():
			print("Song is over... :(")
			music_child = startMusic(SONG_NUM)
		
		# Check for AWS commands that have not been processes
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
			elif message == " ": #pause music
				output = music_child.changeMusicOutput(message)
			elif message == "=": #increase volume
				if not MAX_VOLUME_REACHED:
					output = music_child.changeMusicOutput(message)
				if output == "Current Volume: 6.00dB":
					MAX_VOLUME_REACHED = 1
				if MIN_VOLUME_REACHED:
					MIN_VOLUME_REACHED = 0
				print(output)
			elif message == "-": #decrease volume
				if not MIN_VOLUME_REACHED:
					output = music_child.changeMusicOutput(message)
				if output == "Current Volume: -51.00dB":
					MIN_VOLUME_REACHED = 1
				if MAX_VOLUME_REACHED:
					MAX_VOLUME_REACHED = 0
				print(output)
			

		# Start new recording process if last recording has finished.
		if FINISHED_RECORDING == 1:
			#create thread which will handle the recording subprocess
			FINISHED_RECORDING = 0
			x = threading.Thread(target=RecordChild, args=(RECORDING_LENGTH,"rec{}".format(REC_COUNT)))
			x.start()

		# Check if there are recordings that need to be sent to AWS
		if not RECORD_QUEUE.empty():
			#create thread to send recording
			x = threading.Thread(target=sendRecording, args=(RECORD_QUEUE.get(),))
			x.start()
		
		# If connection with AWS is lost, attempt to restablish
		if LOST_CONNECTION_FLAG:
			LOST_CONNECTION_FLAG = 0
			command_thread = threading.Thread(target=controlInterface, args=())
			command_thread.start()