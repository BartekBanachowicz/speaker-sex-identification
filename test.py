# This script automatically tests solution with available training set
# ---------

from __future__ import division
import numpy as np
from os import listdir
from os.path import isfile, isdir, join, dirname, basename
import re
import librosa
import sys


def recognize(file_path):
    audio_signal, sampling_rate = librosa.load(file_path)
    f0, voiced_flag, voiced_probs = librosa.pyin(audio_signal, fmin=70, fmax=300)

    print("File: ", file_path)

    f0 = f0[~np.isnan(f0)]
    if len(f0) == 0:
        f0_mean = 0
    else:
        f0_mean = sum(f0) / len(f0)
        print("f0 mean: ", f0_mean)

    if f0_mean > 170:
        sex = "K"
    else:
        sex = "M"

    print("Answer: ", sex)
    return sex


def check_if_correct(path, result):
    pattern = re.compile(".+M.+")
    sex = "K"
    if pattern.match(basename(path)):
        sex = "M"
    print("Correct answer:", sex)

    if result == sex:
        print("SUCCESS\n")
        return 1
    else:
        print("FAIL\n")
        return 0


def check_sex(path):
    pattern = re.compile(".+M.+")
    if pattern.match(basename(path)):
        return 'M'
    else:
        return 'F'


if __name__ == '__main__':
    path = join(dirname(__file__), sys.argv[1])

    male = []
    female = []

    if isdir(path):
        files = listdir(path)
        n = len(files)
        success_count = 0
        for f in files:
            success_count += check_if_correct(join(path, f), recognize(join(path, f)))
            # sex, mean = recognize(join(path, f))
            #
            # if mean != 0:
            #     if sex == 'F':
            #         female.append(mean)
            #     elif sex == 'M':
            #         male.append(mean)

        print("{}/{} test passed\nSuccess rate: {}%\n".format(success_count, n, success_count / n * 100))
        # print(f"FEMALE\n\tmean: {sum(female)/len(female)}\n\tmin: {min(female)}\n\tmax: {max(female)}")
        # print(f"FEMALE\n\tmean: {sum(male)/len(male)}\n\tmin: {min(male)}\n\tmax: {max(male)}")

        # fig, ax = plt.subplots(1, 2)
        # ax[0].hist(male)
        # ax[1].hist(female)
        # plt.show()


    elif isfile(path):
        check_if_correct(path, recognize(path))
