# This script prepares the ESC50 data set (https://github.com/karolpiczak/ESC-50)
# for use with the TinyML speech recognition example
# (https://github.com/tensorflow/tflite-micro/blob/main/tensorflow/lite/micro/examples/micro_speech/train/train_micro_speech_model.ipynb)
# It has four main steps
# 1. split ESC50 files into 1-second clips
# 2. ignore silent clips
# 3. resample to 16000 Hz
# 4. save non-silent, 16hHz, 1-second clips into separate directories according to training label
# The removal of silent clips is necessary, because many ESC50 clips contain silence especially at the end.
# The parameters (min_silence_length and silence_threshold) are derived from trial and error
# and will be different for other data sets.

import os
import csv
from pydub import AudioSegment, silence
from pydub.utils import make_chunks

chunk_length_ms = 1000 # pydub calculates in millisec
min_silence_length = 500
silence_threshold = -30
sample_rate = 16000
in_directory = "...\\ESC-50-master" # path to directory with ESC50
audio_directory = in_directory + "\\audio"
metadata_file = in_directory + "\\meta\\esc50.csv"
out_directory = ".\\esc50_data_processed" # new output directory

# read CSV with metadata
with open(metadata_file, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')

    # iterate over CSV rows reading filename and category, skipping header
    next(csvreader)
    for row in csvreader:
        filename = row[0]
        category = row[3]
        print(filename, category)

        # check if target folder exists, if not, create
        if not os.path.isdir(out_directory + os.sep + category):
            os.makedirs(out_directory + os.sep + category)

        # read file
        myaudio = AudioSegment.from_file(audio_directory + os.sep + filename, "wav")

        # chunking
        chunks = make_chunks(myaudio, chunk_length_ms)

        # iterate over chunks
        for i, chunk in enumerate(chunks):

            # check for silence, if silence, skip to next chunk
            if not silence.detect_silence(chunk, min_silence_len=min_silence_length, silence_thresh=silence_threshold):
                chunk_name = out_directory + os.sep + category + os.sep + "{0}-chunk{1}.wav".format(filename[:-4], i)
                # print(chunk_name)
                # resample
                chunk_resampled = chunk.set_frame_rate(sample_rate)
                # print(chunk_resampled.frame_rate
                # export to wav
                chunk_resampled.export(chunk_name, format="wav")

