import os
import sys
import mido
sys.path.append('..')
from _utils import *

"""
[Definitions]
    BPM: beats per minute
    TPB: ticks per beat
    tempo: μs per beat

[Default values]
    1 beat = 1 quater-note = 6 MIDI clocks

    tempo = 500000 
    -> 500000 μs (0.5s) per beat
    -> 1 minute per 120 beats
    -> BPM = 120

    ticks per beat = ?

[Example]
    ticks_per_beat = 480
    tempo = μs_per_beat = 800000
    -> 1 tick = μs_per_beat / ticks_per_beat ≈ 1666.67 μs

"""

fn = 'passionate-duelist.mid'

md = mido.MidiFile(fn)

tracks = md.tracks

print(len(tracks), md.length, md.ticks_per_beat)

def disp_track(trk):
    with open('tracks.log', 'w') as wf:
            # trk = sorted(trk, key=lambda msg: msg.time)
            # print(trk, file=wf)
            print(len(trk), file=wf)
            for msg in trk:
                print(f'\t{msg.type} {msg}', file=wf)

def disp_program(msg):
    if msg.type == 'program_change':
        prog = msg.program
        chan = msg.channel
        if chan == 9:
            inst = percussion_num_table[prog]
        else:
            inst = patch_num_table[prog]

        # print(f'channel: {chan:<3} program: {prog:<4} instrument: {inst}')

disp_track(tracks[0])