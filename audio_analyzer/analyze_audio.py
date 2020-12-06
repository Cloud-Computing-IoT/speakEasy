# ENSURE YOU ARE USING TENSORFLOW 1.14
#
# USE:
#
# import analyze_audio
# results_dict = analyze_audio.run("recording.wav")

import subprocess

from classifier import inference

def run(input_filename):
    # Feature extraction
    subprocess.run(['feature_extraction/vggish_inference_demo.py',
                    '--wav_file', '/Users/tristanelma/My_stuff/EE_542/final_project/system/' + input_filename,
                    '--tfrecord_file', 'extracted_features.tfrecord',
                    '--pca_params', '/Users/tristanelma/My_stuff/EE_542/final_project/system/feature_extraction/vggish_pca_params.npz',
                    '--checkpoint', '/Users/tristanelma/My_stuff/EE_542/final_project/system/feature_extraction/vggish_model.ckpt'
                    ])

    # Classification/inference
    results = inference.main()

    return results

# if __name__ == "__main__":
#     results = run('Another_day_no_voice.wav')
#     print(results)