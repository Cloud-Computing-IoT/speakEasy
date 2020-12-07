# Controller script for speaker

from audio_analyzer import analyze_audio


if __name__ == "__main__":
    results = analyze_audio.run('Another_day_w_voice_close.wav')
    print(results)
