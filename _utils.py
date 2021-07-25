import os
import sys

def color_print(s, level='info'):
    msg_level_D = {
        'shell'  : '1;34;40',
        'success': '1;32;40',
        'info'   : '1;36;40',
        'warn'   : '1;35;40',
        'error'  : '1;31;40',
    }
    cb = '\x1b[{}m'
    ce = '\x1b[0m'
    
    # cb = cb.format('1;33;40')
    cb = cb.format(msg_level_D[level])
    print(f'{cb}{s}{ce}')

def disp_dict(data):
    max_len = len(max(data, key=len))
    for k,v in data.items():
        color_print(f'{k:{max_len+1}}: {v}', level='info')

# General MIDI numbers
#   https://pjb.com.au/muscript/gm.html

# General MIDI Percussion and Sounds
#   https://jazz-soft.net/demo/GeneralMidiPerc.html
#   https://jazz-soft.net/demo/GeneralMidi.html

# Standard MIDI file format, updated
#   http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html
midi_patch_number_table = {

}