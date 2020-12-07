# Reguirements:
# Python 3.7, TensorFlow 1.14, numpy, resampy, tf_slim, six, soundfile
#
# Usage example:
# import analyze_audio
# results_dict = analyze_audio.run("recording.wav")

# This file provides an interface to the feature extractor and classifier programs

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