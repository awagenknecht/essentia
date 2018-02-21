#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Created by pablo on 2/02/18

"""
This script find all the files in a folder, tries to open them as audio files,
set some samples to 0 in order to generate a gap and ens and saves them in a desired folder
"""

import numpy as np
import os
import essentia.standard as es
from essentia import array as esarr


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if basename.lower().endswith(pattern):
                filename = os.path.join(root, basename)
                yield filename


if __name__ == '__main__':
    in_folder = '../../audio/recorded'
    out_folder = '../../QA-audio/Gaps/'
    fs = 44100.
    files = [x for x in find_files(in_folder, 'wav')]
    if not files:
        print('no files found!')

    for f in files:
        try:
            audio = es.MonoLoader(filename=f, sampleRate=fs)()
        except Exception:
            print '{} was not loaded'.format(f)
            continue

        original_len = len(audio)

        start_jump = original_len/4

        end_jump = start_jump + int(np.abs(np.random.randn()) * fs)

        audio[start_jump:end_jump] = np.zeros(end_jump - start_jump)

        text = ['{}\t{}\tevent\n'.format(start_jump/float(fs), end_jump/float(fs))]

        if not os.path.exists(out_folder):
            os.mkdir(out_folder)

        f_name = ''.join(os.path.basename(f).split('.')[:-1])
        with open('{}/{}_gap.lab'.format(out_folder, f_name), 'w') as o_file:
            o_file.write(''.join(text))

        es.MonoWriter(filename='{}/{}_gap.wav'.format(out_folder, f_name))(esarr(audio))
