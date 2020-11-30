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
#os.system("omxplayer mp3_test.mp3")
#omxprocess = subprocess.Popen(['omxplayer', music_path],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def spawnMusicChild(self):
	child = pexpect.spawn('omxplayer ' + MUSIC_PATH.format(music = sample_music))
	return child

def spawnRecordingChild(self, record_time, file_name):
	child = pexpect.spawn(RECORD_COMMAND.format(time = record_time, file = file_name))
	return child

def changeMusicOutput(self, command, musicChild):
	music_child.send(command)
	print(music_child.before)

def terminateProcess(self, child):
	child.close()


if __name__ == '__main__':
	music_child = spawnMusicChild()
	# recording_child = spawnRecordingChild()
	changeMusicOutput(VOLUME_DOWN, music_child)
	time.sleep(2)
	changeMusicOutput(VOLUME_DOWN, music_child)
	time.sleep(2)
	terminateProcess(music_child)

# time.sleep(2)
# child.send('-')
# child.send('-')
# child.send('-')
# child.send('-')
# time.sleep(2)
# child.send(' ')
# time.sleep(5)
# child.send(' ')
# child.send('=')
# child.send('=')
# child.send('=')
# child.send('=')
# time.sleep(2)
#child.terminate()
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

#for i in range(3):
	#print("Here")
#	time.sleep(1)
#	omxprocess.stdin.write('='.encode())
#	try:
		#output = omxprocess.communicate(input='='.encode())[0]
		#omxplayer.check_call('='.encode())
		#print("increased volume")
#	except:
		#print(output)

#for i in range(3):
#	time.sleep(1)
	#omxprocess.stdin.write('-'.encode())
#	output = omxprocess.communicate(input='-'.encode())[0]
#	priint("decreased volume")

#omxprocess.communicate(input='q'.encode())[0]
#omxprocess.kill()
