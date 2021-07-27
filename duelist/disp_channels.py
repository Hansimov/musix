import os
import sys
import mido
sys.path.append('..')
from _utils import *

fn = 'passionate-duelist.mid'

md = mido.MidiFile(fn)

# tracks = md.tracks
tracks = md.tracks
print(len(tracks))
trk = tracks[1]
# print(trk)

cnt = 0
for trk in tracks:
    for msg in trk:
        if msg.type == 'program_change':
            prog = msg.program
            chan = msg.channel
            if chan == 9:
                inst = percussion_num_table[prog]
            else:
                inst = patch_num_table[prog]

            print(f"channel: {chan:<3} program: {prog:<4} instrument: {inst}")
            cnt += 1
print(cnt)

# for func in dir(md):
#     print(func)

# for i in range(10000):
#     print(i)
