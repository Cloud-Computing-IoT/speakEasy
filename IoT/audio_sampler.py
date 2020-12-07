import music_test as m 
import time

SONG1 = "mp3_test.mp3"
SONG2 = "Lite_Weight.mp3"
SONG3 = "24kGoldn.mp3"
SONG4 = "Another_day.mp3"
SONG5 = "DragonForce.mp3"

c = m.MusicChild(SONG4)
r = m.RecordChild(10,"Another_day_no_voice")

# c = m.MusicChild(SONG5)
# r = m.RecordChild(10,"DragonForce_no_voice")

time.sleep(15)