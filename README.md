# speakEasy

Final Project for EE 542 at the University of Southern California

Matt Pisini, Charlie Bennett, Tristan Elma


**speakEasy** is a smart speaker controller that adjusts speaker volume in real-time, based on audio and accelerometer data collected from the area around it. This code was designed and tested on an Amazon EC2 instance (t2.xlarge) running Ubuntu 16.04, interfacing with an RPi that is connected to the speaker and microphone, as well as Android phones which gather accelerometer data through Termux and communicate it to the cloud using Netcat.


Requirements:
- Python 3.7, TensorFlow 1.14, numpy, resampy, tf_slim, six, soundfile
- Install TensorFlow 1.14:
`python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.14.0-py3-none-any.whl`


Instructions:
- The code assumes the repo is cloned into /home/ubuntu/EE542_final_project/Cloud-Enabled-Smart-Speaker/ .
- Establish TCP connections from RPi and Androids to supply audio and accelerometer data
- Begin the main program:
`python3 controller_working.py`


Credit:
Audio training data, audio feature extractor, and audio classifier adapted from the AudioSet and YouTube-8M projects from Google:
- AudioSet:
    - GitHub: https://github.com/tensorflow/models/tree/master/research/audioset
    - Paper: https://research.google.com/pubs/pub45857.html
    - Authors:
        - Dan Ellis
        - Shawn Hershey
        - Aren Jansen
        - Manoj Plakal
- YouTube-8M:
    - GitHub: https://github.com/google/youtube-8m
    - Paper: https://arxiv.org/abs/1609.08675