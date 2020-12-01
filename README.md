# Cloud-Enabled-Smart-Speaker


Audio Sample Google Drive Folder:
https://drive.google.com/drive/u/1/folders/1DA_jWyUNl5f5mxwNiFI4wogO564nuH4U



AudioSet Dataset:
https://research.google.com/audioset/download.html

Feature Extractor Program (this takes in your audio files and generates the 128-D features for each second):
https://github.com/tensorflow/models/tree/master/research/audioset/vggish

Classifier Starter Code:
https://github.com/google/youtube-8m
Note: I've noticed bugs in the classifier starter code due to old TensorFlow code (version 1.0), that no longer works. We'll likely have to tweak it to upgrade it to TF 2.0 and also to work with our audio data only.

Here is the YouTube8M Dataset, which is very similar dataset to AudioSet, except that it has both video (rgb) and audio annotations (with the same format as AudioSet).
I've included this because this is the dataset used by the classifier starter code, though it can likely be modified to work with AudioSet.
YouTube8M Dataset (see "Frame-level features dataset"): https://research.google.com/youtube8m/download.html

