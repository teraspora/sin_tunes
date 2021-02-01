# sin_tunes
# Test creating sine wave and geberating notes of the scale
# John Lynch
# Jan./Feb. 2021

import sys
import numpy as np
from scipy.io.wavfile import write


SAMPLE_RATE = 44100
base_tone = 220.
# Represent note sequences as strings, e.g. 'acef+gf+ecab-2'
scale = ['a', 'b-', 'b', 'c', 'c+', 'd', 'e-', 'e', 'f', 'f+', 'g', 'a-']
tones = {}

def init():
    for index, note in enumerate(scale):
        tones[note] = base_tone * 2. ** (index / 12.)
        tones[note.upper()] = tones[note] * 2   # uppercase means an octave higher

def get_tone(note, duration=0.25):
    return w_sq(tones[note], duration)

def write_tune(note_seq, output_file):
    note_list = []
    str_len = len(note_seq)
    for i, ch in enumerate(note_seq):
        if ch in ['-+']:
            continue
        if ch in 'abcdefgABCDEFG':
            if i + 1 < str_len and (next_ch := note_seq[i + 1]) in '-+':
                note_list.append(ch + next_ch)
            else:
                note_list.append(ch)
    # print(note_list)
    # sys.exit(0)
    tune = np.array([])
    for note in note_list:
        tune = np.concatenate((tune, get_tone(note)))
    write(output_file, SAMPLE_RATE, tune)

def w_sin(freq=440, duration=1.0, sample_rate=44_100):
    """
    Return a sine wave with the given parameters as a numpy array
    """
    num_samples = np.arange(sample_rate * duration)
    sin_wave = np.sin(2 * np.pi * num_samples * freq / sample_rate) * 0.1
    sin_wave_i16 = np.int16(sin_wave * 1024)
    return sin_wave_i16

def w_sq(freq=440, duration=1.0, sample_rate=44_100):
    """
    Return a sine wave with the given parameters as a numpy array
    """
    num_samples = np.arange(sample_rate * duration)
    phi = 2 * np.pi * num_samples * freq / sample_rate
    sin_wave = (np.sin(phi) + 0.333333 * np.sin(3 * phi) + 0.2 * np.sin(5 * phi) + 0.142857 * np.sin(7 * phi)) * 0.1
    sin_wave_i16 = np.int16(sin_wave * 1024)
    return sin_wave_i16

if __name__ == '__main__':
    init()
    while tune := input('Enter tune:  '):
        write_tune(tune, f'tune_{tune}.wav')
