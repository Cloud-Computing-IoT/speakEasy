# ENSURE YOU ARE USING TENSORFLOW 1.14
#
# USE:
#
# import analyze_audio
# results_dict = analyze_audio.run("recording.wav")

import subprocess
import pathlib
import os

from audio_analyzer.classifier import inference

def run(input_filename, begin_flag):
    proj_dir = '/home/ubuntu/EE542_final_project/Cloud-Enabled-Smart-Speaker/audio_analyzer'
    # Feature extraction
    subprocess.run([os.path.join(proj_dir, 'feature_extraction/vggish_inference_demo.py'),
                    '--wav_file', os.path.join(proj_dir, input_filename),
                    '--tfrecord_file', os.path.join(proj_dir, 'extracted_features.tfrecord'),
                    '--pca_params', os.path.join(proj_dir, 'feature_extraction/vggish_pca_params.npz'),
                    '--checkpoint', os.path.join(proj_dir, 'feature_extraction/vggish_model.ckpt')],
		    stdout = subprocess.DEVNULL)               

    # Classification/inference
    results = inference.classify_run1(begin_flag)

    return results

if __name__ == "__main__":
    results = run('Another_day_no_voice.wav')
    print(results)
