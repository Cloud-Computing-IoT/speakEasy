import os
import time
import pexpect
import TCP as tcp

TCP_IP = "192.168.86.26"
TCP_PORT = 5005

HOME_DIREC = "/home/pi/"
MUSIC_PATH = "/home/pi/{music}"
OMXPLAYER_START = "delay: 0\r\n"
RECORD_START = "Stereo\r\n"
sample_music = "mp3_test.mp3"
RECORD_COMMAND = "arecord -D hw:1,0 -d {time} -f cd {file_path}{file}.wav"
VOLUME_UP = '='
VOLUME_DOWN = '-'
PAUSE = ' '

class MusicChild:
	def __init__(self):
		self.child = pexpect.spawn('omxplayer ' + MUSIC_PATH.format(music = sample_music))
		self.child.expect(OMXPLAYER_START)

	def changeMusicOutput(self, command):
		self.child.send(command)
		if command = " ":
			output = None
		else: 
			self.child.expect("\r\n")
			output = self.child.before.decode()
		return output

	def terminateProcess(self):
		self.child.close()

class RecordChild:
	def __init__(self, record_time, file_name):
		self.child = pexpect.spawn(RECORD_COMMAND.format(time = record_time, file_path = HOME_DIREC, file = file_name))
		# this process will automatically terminate after it records for 'record_time'



if __name__ == '__main__':

	AWS_socket = tcp.TCPsocket()
	AWS_socket.connect(TCP_IP, TCP_PORT)
	# AWS_socket.sendFile(HOME_DIREC + "test.wav")
	# PATH = "/Users/matthewpisini/Desktop/DPunk.mp3"
	# AWS_socket.sendFile(PATH)
	music_child = MusicChild()
	AWS_socket.sendMessage("Started music with song " + sample_music)

	while True:
		message = AWS_socket.receiveMessage()
		print(message)
		if message == "stop":
			AWS_socket.sendMessage("Terminating program now.")
			AWS_socket.closeSocket()
			music_child.terminateProcess()
			break
		elif message == "=" or "-" or " ":
			output = music_child.changeMusicOutput(message)
			print(output)
			if message == "=":
				AWS_socket.sendMessage("Increased volume")
			if message == "-":
				AWS_socket.sendMessage("Decreased volume")
			if message == " ":
				AWS_socket.sendMessage("Paused music")
		elif message.lower() == "record":
			recording_child = RecordChild(5,"test")
			AWS_socket.sendMessage("Recording...")

		# AWS_socket.sendMessage(message)
	# recording_child = RecordChild(5,"test")
	# # recording_child.terminateProcess()
	# for i in range(5):
	# 	time.sleep(1)
	# 	music_child.changeMusicOutput(VOLUME_DOWN)
	# time.sleep(5)
	# music_child.terminateProcess()