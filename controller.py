# Controller script for speaker

from audio_analyzer import analyze_audio

if __name__ == "__main__":

    volume = 5
    while(True):
        # Retrieve data from mic and accelerometers

        input_audio_file = 'Another_day_w_voice_close.wav'

        # Analyze audio to determine which sound classes it contains
        results = analyze_audio.run(input_audio_file)

        # Process audio class results to adjust volume
        # Relevant classes:
        #   0: speech, 4: conversation, 16: laughter, 66: cheering, 137: music, 138: musical instrument
        volume_adjustment_audio = 0
        if(results[0] > .3):
            print("speech detected")
            volume_adjustment_audio = -1
        if results[66] > .1 or results[16] > .1:
            print("cheering or laughter detected")
            volume_adjustment_audio = 1

        # Process accelerometer data to adjust volume
        volume_adjustment_accelerometer = 0

        
        # Adjust volume
        volume += volume_adjustment_audio
        volume += volume_adjustment_accelerometer
        if(volume < 1):
            volume = 1
        elif(volume > 10):
            volume = 10

        # Send command to speaker to adjust volume
        print(volume)
