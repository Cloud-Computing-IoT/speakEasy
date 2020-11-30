import os
import sys

os.system("arecord -D hw:1,0 -d 5 -f cd test.wav")
