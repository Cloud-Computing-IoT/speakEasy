# Reguirements:
# Python 3.7, TensorFlow 1.14, numpy, resampy, tf_slim, six, soundfile
#
# Usage example:
# import analyze_audio
# results_dict = analyze_audio.run("recording.wav")
#
# - Audio feature extractor adapted from the AudioSet project from Google:
#     - GitHub: https://github.com/tensorflow/models/tree/master/research/audioset
#     - Paper: https://research.google.com/pubs/pub45857.html
#     - Authors:
#         - Dan Ellis
#         - Shawn Hershey
#         - Aren Jansen
#         - Manoj Plakal
# - Classifier code adapted from YouTube-8M project from Google:
#     - GitHub: https://github.com/google/youtube-8m
#     - Paper: https://arxiv.org/abs/1609.08675

# Wrapper interface to run both the feature extractor and classifier programs
# to extract audio class information from an input audio recording

import subprocess
import pathlib
import os

from audio_analyzer.classifier import inference

def run(input_filename, begin_flag):
    proj_dir = pathlib.Path(__file__).parent.absolute()

    # Call feature extraction program
    subprocess.run([os.path.join(proj_dir, 'feature_extraction/vggish_inference_demo.py'),
                    '--wav_file', os.path.join(proj_dir, input_filename),
                    '--tfrecord_file', 'extracted_features.tfrecord',
                    '--pca_params', os.path.join(proj_dir, 'feature_extraction/vggish_pca_params.npz'),
                    '--checkpoint', os.path.join(proj_dir, 'feature_extraction/vggish_model.ckpt')
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Call classification/inference program
    results = inference.classify_run(begin_flag)

    return results
