import os
import sys
import subprocess
import time
import pexpect
from multiprocessing import Process


MUSIC_PATH = "/home/pi/{music}"
sample_music = "mp3_test.mp3"
RECORD_COMMAND = "arecord -D hw:1,0 -d {time} -f cd {file_name}.wav"
VOLUME_UP = '='
VOLUME_DOWN = '-'
PAUSE = ' '

class MusicChild:
	def __init__(self):
		self.child = pexpect.spawn('omxplayer ' + MUSIC_PATH.format(music = sample_music))

	def changeMusicOutput(self, command):
		self.child.send(command)
		print(self.child.read())

	def terminateProcess(self):
		self.child.close()

# def spawnRecordingChild(self, record_time, file_name):
# 	child = pexpect.spawn(RECORD_COMMAND.format(time = record_time, file = file_name))
# 	return child

if __name__ == '__main__':
	music_child = MusicChild()
	# recording_child = spawnRecordingChild()
	music_child.changeMusicOutput(VOLUME_DOWN)
	time.sleep(2)
	music_child.changeMusicOutput(VOLUME_DOWN)
	time.sleep(2)
	music_child.terminateProcess()

#omxprocess.call(input='-'.encode())
#omxprocess.stdin.write('-'.encode())
#time.sleep(1)
#print(omxprocess.stdout)
#omxprocess.stdin.write('-'.encode())
#time.sleep(1)
#omxprocess.stdin.write('-'.encode())
#omxprocess.stdin.write('-'.encode())
#output = omxprocess.communicate(input='-'.encode())[0]
#output = omxprocess.communicate(input='='.encode())[0]
