import os
import sys
import mido
sys.path.append('..')
from _utils import *

fn = 'passionate-duelist.mid'

md = mido.MidiFile(fn)

tracks = md.tracks
print(len(tracks))

def disp_track(trk):
    with open('tracks.log', 'w') as wf:
        for trk in tracks:
            # trk = sorted(trk, key=lambda msg: msg.time)
            # print(trk, file=wf)
            print(len(trk), file=wf)
            for msg in trk:
                print(f'\t{msg.type} {msg}', file=wf)

def disp_track_x():
    cnt = 0
    for trk in tracks:
        # print(len(trk))
        for msg in trk:
            if msg.type == 'program_change':
                prog = msg.program
                chan = msg.channel
                if chan == 9:
                    inst = percussion_num_table[prog]
                else:
                    inst = patch_num_table[prog]

                # print(f'channel: {chan:<3} program: {prog:<4} instrument: {inst}')
                cnt += 1
        # print(cnt)

disp_track(tracks[1])