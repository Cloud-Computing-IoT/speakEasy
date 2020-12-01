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
SCP = "scp {file} {hostname}@{ip_addr}:{dest_direc}"

class MusicChild:
	def __init__(self):
		self.child = pexpect.spawn('omxplayer ' + MUSIC_PATH.format(music = sample_music))
		self.child.expect(OMXPLAYER_START)

	def changeMusicOutput(self, command):
		self.child.send(command)
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

	AWS_socket = tcp.TCPsocket(TCP_IP, TCP_PORT)
	AWS_socket.sendFile(HOME_DIREC + "test.wav")
	# music_child = MusicChild()
	# recording_child = RecordChild(5,"test")
	# # recording_child.terminateProcess()
	# for i in range(5):
	# 	time.sleep(1)
	# 	music_child.changeMusicOutput(VOLUME_DOWN)
	# time.sleep(5)
	# music_child.terminateProcess()