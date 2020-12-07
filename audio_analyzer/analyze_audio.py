# ENSURE YOU ARE USING TENSORFLOW 1.14
#
# USE:
#
# import analyze_audio
# results_dict = analyze_audio.run("recording.wav")

import subprocess
import pathlib
import os

from classifier import inference

def run(input_filename):
    proj_dir = pathlib.Path(__file__).parent.absolute()
    # Feature extraction
    subprocess.run(['feature_extraction/vggish_inference_demo.py',
                    '--wav_file', os.path.join(proj_dir, input_filename),
                    '--tfrecord_file', 'extracted_features.tfrecord',
                    '--pca_params', os.path.join(proj_dir, 'feature_extraction/vggish_pca_params.npz'),
                    '--checkpoint', os.path.join(proj_dir, 'feature_extraction/vggish_model.ckpt')
                    ])

    # Classification/inference
    results = inference.main()

    return results

if __name__ == "__main__":
    results = run('Another_day_w_voice_close.wav')
    print(results)
