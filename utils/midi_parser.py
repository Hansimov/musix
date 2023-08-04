import mido

"""
[Definitions]
    BPM: beats per minute
    TPB: ticks per beat
    tempo: μs per beat

[Default values]
    1 beat = 1 quarter-note = 6 MIDI clocks

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


""" [The structure of MidiFile in mido]

* Standard MIDI Files — Mido 1.3.0 documentation
  * https://mido.readthedocs.io/en/stable/files/midi.html

MidiFile > MidiTracks > Messages

MidiFile: [type, ticks_per_beat, tracks]
Message:
  - type: (meta) 'time_signature'
    - numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0
  - type: (meta) 'key_signature'
    - key='B', time=0
  - type: 'control_change'
    - channel=0, control=121, value=0, time=0
  - type: 'program_change'
    - channel=0, program=40, time=0
  - type: (meta) 'midi_port'
    - port=0, time=0
  - type: 'set_tempo'
    - tempo=419581, time=1890
  - type: 'note_on'
    - channel=0, note=83, velocity=85, time=14670
  - type: (meta) 'end_of_track'
    - time=1


## Example:

`mido.MidiFile(midi_filepath)`

MidiFile(type=1, ticks_per_beat=480, tracks=[
  MidiTrack([
    MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0),
    MetaMessage('key_signature', key='B', time=0),
    Message('control_change', channel=0, control=121, value=0, time=0),
    Message('program_change', channel=0, program=40, time=0),
    ...
    MetaMessage('midi_port', port=0, time=0),
    Message('control_change', channel=1, control=121, value=0, time=0),
    Message('program_change', channel=1, program=45, time=0),
    ...
    MetaMessage('midi_port', port=0, time=0),
    MetaMessage('set_tempo', tempo=419581, time=1890),
    Message('note_on', channel=0, note=83, velocity=85, time=14670),
    ...
    Message('note_on', channel=0, note=80, velocity=0, time=0),
    MetaMessage('end_of_track', time=1)
  ]),
  MidiTrack([
    MetaMessage('key_signature', key='B', time=0),
    Message('control_change', channel=3, control=121, value=0, time=0),
    Message('program_change', channel=3, program=38, time=0),
    ...
    MetaMessage('end_of_track', time=1)
  ]),
  ...
  MidiTrack([
    MetaMessage('key_signature', key='B', time=0),
    MetaMessage('midi_port', port=2, time=0),
    Message('note_on', channel=6, note=60, velocity=62, time=198960),
    ...
    MetaMessage('end_of_track', time=1)
  ])
])
    
"""


class MidiParser:
    def __init__(self, midi_filepath):
        self.midi_filepath = midi_filepath
        self.mf = mido.MidiFile(self.midi_filepath)

    def run(self):
        mf = self.mf
        print(mf)
