# sin_tunes
# Test creating sine wave and geberating notes of the scale
# John Lynch
# Jan./Feb. 2021
# Example tune: adedc+baAAABC+DAgf+edc+bc+babc+dedc+baAAABC+DAgf+edc+ddddd

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

def w_sin(freq=440, duration=0.25, sample_rate=44_100):
    """
    Return a sine wave with the given parameters as a numpy array
    """
    num_samples = np.arange(sample_rate * duration)
    wave = np.sin(2 * np.pi * num_samples * freq / sample_rate) * 0.1
    wave_i16 = np.int16(wave * 1024)
    return wave_i16

def w_sq(freq=440, duration=0.25, sample_rate=44_100):
    """
    Return a square wave with the given parameters as a numpy array
    """
    num_samples = np.arange(sample_rate * duration)
    phi = 2 * np.pi * num_samples * freq / sample_rate
    # Square wave has only the odd harmonics
    wave = np.sin(phi)
    for n in range(3, 31, 2):
        wave += 1 / n * np.sin(n * phi)
    wave_i16 = np.int16(wave * 1024)
    return wave_i16

def w_saw(freq=440, duration=0.25, sample_rate=44_100):
    """
    Return a sawtooth wave with the given parameters as a numpy array
    """
    num_samples = np.arange(sample_rate * duration)
    phi = 2 * np.pi * num_samples * freq / sample_rate
    wave = np.sin(phi)  # the coefficient 2 for first harmonic makes a big difference; need to check this series
    for n in range(2, 16):
        wave += 2 / n * (-1) ** (n + 1) * np.sin(n * phi)
    wave_i16 = np.int16(wave * 1024)
    return wave_i16

def get_tone(note, duration=0.25, wave_function=w_sin):
    return wave_function(tones[note], duration)

def write_tune(note_seq, output_file, duration=0.25, wave_function=w_sin):
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
    tune = np.array([])
    for note in note_list:
        tune = np.concatenate((tune, get_tone(note, duration, wave_function)))
    write(output_file, SAMPLE_RATE, tune)

if __name__ == '__main__':
    init()
    waves = {'sin': w_sin, 'sq': w_sq, 'saw': w_saw}
    w_func = w_sin if (w_func := input('Wave type? (sin, sq or saw):  ')) not in waves else waves[w_func]
    while tune := input('Enter tune:  '):
        write_tune(tune, f'tune_{w_func.__name__[2:]}_{tune}.wav', 0.25, w_func)
