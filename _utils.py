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


# Standard MIDI file format, updated
#   http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html

# General MIDI Percussion and Sounds
#   https://jazz-soft.net/demo/GeneralMidi.html
#   https://jazz-soft.net/demo/GeneralMidiPerc.html

# General MIDI numbers
#   https://pjb.com.au/muscript/gm.html

# GM 1 Sound Set
#   https://www.midi.org/specifications-old/item/gm-level-1-sound-set

# Music Representation Labs
#   http://www.ccarh.org/courses/253/handout/gminstruments/

patch_num_table = {
# Piano
    0: 'Acoustic Grand Piano',
    1: 'Bright Acoustic Piano',
    2: 'Electric Grand Piano',
    3: 'Honky-tonk Piano',
    4: 'Rhodes Piano',
    5: 'Chorused Piano',
    6: 'Harpsichord',
    7: 'Clavinet',
# Chromatic
    8 : 'Celesta',
    9 : 'Glockenspiel',
    10: 'Music Box',
    11: 'Vibraphone',
    12: 'Marimba',
    13: 'Xylophone',
    14: 'Tubular Bells',
    15: 'Dulcimer',
# Organ
    16: 'Hammond Organ',
    17: 'Percussive Organ',
    18: 'Rock Organ',
    19: 'Church Organ',
    20: 'Reed Organ',
    21: 'Accordion',
    22: 'Harmonica',
    23: 'Tango Accordion',
# Guitar
    24: 'Acoustic Nylon Guitar',
    25: 'Acoustic Steel Guitar',
    26: 'Electric Jazz Guitar',
    27: 'Electric Clean Guitar',
    28: 'Electric Muted Guitar',
    29: 'Overdriven Guitar',
    30: 'Distortion Guitar',
    31: 'Guitar Harmonics',
# Bass
    32: 'Acoustic Bass',
    33: 'Fingered Electric Bass',
    34: 'Plucked Electric Bass',
    35: 'Fretless Bass',
    36: 'Slap Bass 1',
    37: 'Slap Bass 2',
    38: 'Synth Bass 1',
    39: 'Synth Bass 2',
# Strings
    40: 'Violin',
    41: 'Viola',
    42: 'Cello',
    43: 'Contrabass',
    44: 'Tremolo Strings',
    45: 'Pizzicato Strings',
    46: 'Orchestral Harp',
    47: 'Timpani',
# Ensemble
    48: 'String Ensemble 1',
    49: 'String Ensemble 2',
    50: 'Synth Strings 1',
    51: 'Synth Strings 2',
    52: 'Choir Aahs',
    53: 'Choir Oohs',
    54: 'Synth Voice',
    55: 'Orchestral Hit',
# Brass
    56: 'Trumpet',
    57: 'Trombone',
    58: 'Tuba',
    59: 'Muted Trumpet',
    60: 'French Horn',
    61: 'Brass Section',
    62: 'Synth Brass 1',
    63: 'Synth Brass 2',
# Reed
    64: 'Soprano Sax',
    65: 'Alto Sax',
    66: 'Tenor Sax',
    67: 'Baritone Sax',
    68: 'Oboe',
    69: 'English Horn',
    70: 'Bassoon',
    71: 'Clarinet',
# Pipe
    72: 'Piccolo',
    73: 'Flute',
    74: 'Recorder',
    75: 'Pan Flute',
    76: 'Bottle Blow',
    77: 'Shakuhachi',
    78: 'Whistle',
    79: 'Ocarina',
# Synth Lead
    80: 'Square Wave Lead',
    81: 'Sawtooth Wave Lead',
    82: 'Calliope Lead',
    83: 'Chiff Lead',
    84: 'Charang Lead',
    85: 'Voice Lead',
    86: 'Fifths Lead',
    87: 'Bass Lead',
# Synth Pad
    88: 'New Age Pad',
    89: 'Warm Pad',
    90: 'Polysynth Pad',
    91: 'Choir Pad',
    92: 'Bowed Pad',
    93: 'Metallic Pad',
    94: 'Halo Pad',
    95: 'Sweep Pad',
# Synth Effects
    96: 'Rain Effect',
    97: 'Soundtrack Effect',
    98: 'Crystal Effect',
    99: 'Atmosphere Effect',
    100: 'Brightness Effect',
    101: 'Goblins Effect',
    102: 'Echoes Effect',
    103: 'Sci-Fi Effect',
# Ethnic
    104: 'Sitar',
    105: 'Banjo',
    106: 'Shamisen',
    107: 'Koto',
    108: 'Kalimba',
    109: 'Bagpipe',
    110: 'Fiddle',
    111: 'Shanai',
# Percussive
    112: 'Tinkle Bell',
    113: 'Agogo',
    114: 'Steel Drums',
    115: 'Woodblock',
    116: 'Taiko Drum',
    117: 'Melodic Tom',
    118: 'Synth Drum',
    119: 'Reverse Cymbal',
# Sound Effects
    120: 'Guitar Fret Noise',
    121: 'Breath Noise',
    122: 'Seashore',
    123: 'Bird Tweet',
    124: 'Telephone Ring',
    125: 'Helicopter',
    126: 'Applause',
    127: 'Gun Shot'
}

percussion_num_table = { # on channel 9 (start from 0)
    0 : '-',
    16: '-',
    27: 'High-Q',
    28: 'Slap',
    29: 'Scratch Push',
    30: 'Scratch Pull',
    31: 'Sticks',
    32: 'Square Click',
    33: 'Metronome Click',
    34: 'Metronome Bell',
    35: 'Acoustic Bass Drum',
    36: 'Bass Drum 1',
    37: 'Side Stick',
    38: 'Acoustic Snare',
    39: 'Hand Clap',
    40: 'Electric Snare',
    41: 'Low Floor Tom',
    42: 'Closed High Hat',
    43: 'High Floor Tom',
    44: 'Pedal High Hat',
    45: 'Low Tom',
    46: 'Open High Hat',
    47: 'Low Mid Tom',
    48: 'High Mid Tom',
    49: 'Crash Cymbal 1',
    50: 'High Tom',
    51: 'Ride Cymbal 1',
    52: 'Chinese Cymbal',
    53: 'Ride Bell',
    54: 'Tambourine',
    55: 'Splash Cymbal',
    56: 'Cowbell',
    57: 'Crash Cymbal 2',
    58: 'Vibraslap',
    59: 'Ride Cymbal 2',
    60: 'High Bongo',
    61: 'Low Bongo',
    62: 'Mute High Conga',
    63: 'Open High Conga',
    64: 'Low Conga',
    65: 'High Timbale',
    66: 'Low Timbale',
    67: 'High Agogo',
    68: 'Low Agogo',
    69: 'Cabasa',
    70: 'Maracas',
    71: 'Short Whistle',
    72: 'Long Whistle',
    73: 'Short Guiro',
    74: 'Long Guiro',
    75: 'Claves',
    76: 'High Wood Block',
    77: 'Low Wood Block',
    78: 'Mute Cuica',
    79: 'Open Cuica',
    80: 'Mute Triangle',
    81: 'Open Triangle',
    82: 'Shaker',
    83: 'Jingle Bell',
    84: 'Bell Tree',
    85: 'Castanets',
    86: 'Mute Surdo',
    87: 'Open Surdo'
}