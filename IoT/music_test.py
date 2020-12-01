import os
import sys
import subprocess
import time
import pexpect
from multiprocessing import Process

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
		self.child.expect("\r\n")
		output = self.child.before.decode()

	def terminateProcess(self):
		self.child.close()

class RecordChild:
	def __init__(self, record_time, file_name):
		self.child = pexpect.spawn(RECORD_COMMAND.format(time = record_time, file_path = HOME_DIREC, file = file_name))
		self.child.expect(RECORD_START)
		time.sleep(record_time)

	def terminateProcess(self):
		self.child.close()

if __name__ == '__main__':
	# music_child = MusicChild()
	recording_child = RecordChild(5,"test")
	recording_child.terminateProcess()
	# music_child.changeMusicOutput(VOLUME_DOWN)
	# time.sleep(2)
	# music_child.changeMusicOutput(VOLUME_DOWN)
	# time.sleep(2)
	# music_child.terminateProcess()