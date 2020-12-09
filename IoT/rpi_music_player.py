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
TCP_PORT = 5005
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

class RecordChild:
	def __init__(self, lock, record_time, file_name):
		global FINISHED_RECORDING
		# FINISHED_RECORDING = 0
		print("starting recording")
		self.child = pexpect.spawn(RECORD_COMMAND.format(time = record_time, file_path = HOME_DIREC, file = file_name))
		self.child.expect(pexpect.EOF)
		global REC_COUNT, RECORD_QUEUE
		print("finished recording {}".format(REC_COUNT))
		lock.acquire()
		RECORD_QUEUE.put("{}{}.wav".format(HOME_DIREC,file_name))
		lock.release()
		REC_COUNT += 1
		if REC_COUNT >= FILE_LIMIT:
			cleanUpRecordings(REC_COUNT-FILE_LIMIT)
			#add how to delete the names off the RECORD_QUEUE
		FINISHED_RECORDING = 1
		# this process will automatically terminate after it records for 'record_time'
		# maybe add automatically sending the file and deleting it?

#probably need to periodically clean up recordings or delete immediately after sending?
def cleanUpRecordings(current_num):
	for file in os.listdir(HOME_DIREC):
		# if ("rec" in file ) and (str(current_num) not in file):
		if "rec{}".format(current_num) in file:
			os.remove(os.path.join(HOME_DIREC, file))

def controlInterface(command_lock, record_lock):
	try:
		AWS_socket = tcp.TCPsocket()
		AWS_socket.connect(AWS_IP, TCP_PORT)
		while True:
			message = AWS_socket.receiveMessage()
			if message.lower() == "file":
				record_lock.acquire()
				AWS_socket.sendFile(RECORD_QUEUE.get())
				record_lock.release()
			elif message in COMMANDS:
				AWS_socket.sendMessage("Received: " + message)
				command_lock.acquire()
				COMMAND_QUEUE.put(message)
				command_lock.release()
				if message.lower() == "stop":
					AWS_socket.closeSocket()
					break
			else:
				AWS_socket.sendMessage("Invalid command: " + message)
	except:
		print("Lost connection to AWS")
		

def startMusic(song_num):
	global SONG_NUM
	music_child = MusicChild(SONG_LIST[SONG_NUM])
	print("Starting music with song: {}".format(SONG_LIST[SONG_NUM]))
	SONG_NUM += 1
	if SONG_NUM >= len(SONG_LIST):
		SONG_NUM = 0
	return music_child
		


if __name__ == '__main__':
	music_child = startMusic(SONG_NUM)

	command_lock = threading.Lock()
	record_lock = threading.Lock()
	# command_thread = spawnThread(controlInterface, [command_lock, record_lock])
	command_thread = threading.Thread(target=controlInterface, args=(command_lock, record_lock))
	command_thread.start()
	# RECORD_QUEUE.put("/home/pi/dummy.txt")
	# command_thread = threading.Thread(target=controlInterface, args=(command_lock,))
	# command_thread.start()
	# AWS_socket.sendMessage("Started music with song " + SONG2)
	# controller = threading.Thread(target=musicControlInterface())
	# controller.start()
	# while True:
	# 	if REC_COUNT >= 5:
	# 		sys.exit(1)
	# 	#creates recording
	# 	if FINISHED_RECORDING == 1:
	# 		print("rec: {}, state: {}".format(REC_COUNT,FINISHED_RECORDING))
			# if REC_COUNT >= FILE_LIMIT:
			# 		cleanUpRecordings(REC_COUNT)
	# 		#create thread which will handle the recording subprocess
	# 		x = threading.Thread(target=RecordChild, args=(RECORDING_LENGTH,"rec{}".format(REC_COUNT)))
	# 		x.start()
	while True:
		if not music_child.child.isalive():
			print("Song is over... :(")
			music_child = startMusic(SONG_NUM)
		
		if not COMMAND_QUEUE.empty():
			command_lock.acquire()
			message = COMMAND_QUEUE.get()
			command_lock.release()
			if message.lower() == "stop":
				music_child.terminateProcess()
				# command_thread.raise_exception()
				command_thread.join()
				print("Shutting down execution...")
				sys.exit(1)
			elif message.lower() == "next":
				music_child.terminateProcess()
				music_child = startMusic(SONG_NUM)
			elif message == "=" or "-" or " ":
				output = music_child.changeMusicOutput(message)
				print(output)
			#maybe do this automatically
			# elif message.lower() == "file":
			# 	AWS_socket.sendFile(HOME_DIREC + "rec{}".format(rec_count))
			# else:
			# 	AWS_socket.sendMessage("Not a command. Try again.")
		if FINISHED_RECORDING == 1:
			# if REC_COUNT >= FILE_LIMIT:
			# 		cleanUpRecordings(REC_COUNT)
			#create thread which will handle the recording subprocess
			FINISHED_RECORDING = 0
			# x = spawnThread(RecordChild,lock=[record_lock],params=[RECORDING_LENGTH,"rec{}".format(REC_COUNT)] )
			x = threading.Thread(target=RecordChild, args=(record_lock, RECORDING_LENGTH,"rec{}".format(REC_COUNT)))
			x.start()