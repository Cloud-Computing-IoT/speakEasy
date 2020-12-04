import os
import time
import pexpect
import TCP as tcp

TCP_IP = "192.168.86.26"
TCP_PORT = 5005

HOME_DIREC = "/home/pi/"
MUSIC_PATH = "/home/pi/{music}"
OMXPLAYER_START = "delay: 0\r\n"
SONG1 = "mp3_test.mp3"
SONG2 = "Lite_Weight.mp3"
SONG3 = "24kGoldn.mp3"
RECORD_COMMAND = "arecord -D hw:1,0 -d {time} -f cd {file_path}{file}.wav"
RECORD_COMMAND2 = "arecord -D hw:1,0 -f cd | nc 192.168.86.26 5005"
VOLUME_UP = '='
VOLUME_DOWN = '-'
PAUSE = ' '
FILE_LIMIT = 5

class MusicChild:
	def __init__(self, sample_music):
		self.child = pexpect.spawn('omxplayer ' + MUSIC_PATH.format(music = sample_music))
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
	def __init__(self, record_time, file_name):
		self.child = pexpect.spawn(RECORD_COMMAND.format(time = record_time, file_path = HOME_DIREC, file = file_name))
		# this process will automatically terminate after it records for 'record_time'
		# maybe add automatically sending the file and deleting it?

#probably need to periodically clean up recordings or delete immediately after sending?
def cleanUpRecordings(current_num):
	for file in os.listdir(HOME_DIREC):
		if ("rec" in file )and (str(current_num) not in file):
			os.remove(os.path.join(HOME_DIREC, file))


if __name__ == '__main__':
	# recording_child = RecordChild(5,"rec{}".format(rec_count))
	recording_child = pexpect.spawn(RECORD_COMMAND2)
	while True:
	"""
	rec_count = 0 #adds number to file recorded
	AWS_socket = tcp.TCPsocket()
	AWS_socket.connect(TCP_IP, TCP_PORT)
	music_child = MusicChild(SONG2)
	AWS_socket.sendMessage("Started music with song " + SONG2)

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
			recording_child = RecordChild(5,"rec{}".format(rec_count))
			rec_count += 1
			AWS_socket.sendMessage("Recording...")
		elif message.lower() == "file":
			AWS_socket.sendFile(HOME_DIREC + "rec{}".format(rec_count))
		else:
			AWS_socket.sendMessage("Not a command. Try again.")

		if rec_count >= FILE_LIMIT:
			cleanUpRecordings(rec_count)

"""