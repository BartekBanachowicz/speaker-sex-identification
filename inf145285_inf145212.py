# Python script to detect speaker sex.
# Script gets relative filepath from input and returns 'K' when female voice or 'M' when male voice e.g.:
# python inf145285_inf145212.py training/001_K.wav
# ------------------------------------------------

import numpy as np
from os.path import isfile, join, dirname
import librosa
import sys
import warnings

warnings.filterwarnings("ignore")

correct_output = False


def recognize(file_path):
    audio_signal, sampling_rate = librosa.load(file_path)
    f0, voiced_flag, voiced_probs = librosa.pyin(audio_signal, fmin=70, fmax=300)

    f0 = f0[~np.isnan(f0)]
    if len(f0) == 0:
        f0_mean = 0
    else:
        f0_mean = sum(f0) / len(f0)

    if f0_mean > 170:
        sex = "K"
    else:
        sex = "M"

    return sex


if __name__ == '__main__':

    if len(sys.argv) > 1:

        path = join(dirname(__file__), sys.argv[1])

        if isfile(path):

            try:
                result = recognize(path)
                if result in ('K', 'M'):
                    correct_output = True
                print(result)

            except:
                correct_output = False

    if not correct_output:
        print('K')
