import os
import sys
import subprocess
import time
import pexpect
from multiprocessing import Process


music_path = "/home/pi/mp3_test.mp3"
#os.system("omxplayer mp3_test.mp3")
#omxprocess = subprocess.Popen(['omxplayer', music_path],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
child = pexpect.spawn('omxplayer /home/pi/mp3_test.mp3')
#def omx_constructor(music_path):
#	os.system('omxplayer ' + music_path) 

#if __name__ == '__main__':
#	p = Process(target = omx_constructor, args = (music_path))
#	p.start()
#	time.sleep(2)

time.sleep(2)
child.send('-')
child.send('-')
child.send('-')
child.send('-')
time.sleep(2)
child.send(' ')
time.sleep(5)
child.send(' ')
child.send('=')
child.send('=')
child.send('=')
child.send('=')
time.sleep(2)
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
