import os


r,w = os.pipe()
process = os.fork()

if process:
	os.close(r)
	w = os.fdopen(w, 'w')
	w.write('=')
else:
	w = os.fdopen(w, 'w')
	w.write("omxplayer mp3_test.mp3")
	r= os.fdopen(r)
