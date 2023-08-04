import mido

""" [Structure of MidiFile in mido]
- Structure:
    - MidiFile > MidiTracks > Messages 

* Standard MIDI Files — Mido 1.3.0 documentation
  * https://mido.readthedocs.io/en/stable/files/midi.html

* Message Types — Mido 1.3.0 documentation
  * https://mido.readthedocs.io/en/stable/message_types.html

* Meta Message Types — Mido 1.3.0 documentation
  * https://mido.readthedocs.io/en/stable/meta_message_types.html?highlight=key_signature

## Example args with values:

- MidiFile:
    - type: 1
        - ticks_per_beat = 480
        - tracks = [...Messages...]
- Message:
    - type: (meta) 'time_signature'
        - numerator = 4
        - denominator = 4
        - clocks_per_click = 24
        - notated_32nd_notes_per_beat = 8
        - time = 0
    - type: (meta) 'key_signature'
        - key = 'B'
        - time = 0
    - type: 'control_change'
        - channel = 0
        - control = 121
        - value = 0
        - time = 0
    - type: 'program_change'
        - channel = 0
        - program = 40
        - time = 0
    - type: (meta) 'midi_port'
        - port = 0
        - time = 0
    - type: (meta) 'set_tempo'
        - tempo = 419581
        - time = 1890
    - type: 'note_on'
        - channel = 0
        - note = 83
        - velocity = 85
        - time = 14670
    - type: (meta) 'end_of_track'
        - time = 1


## Example console output:

`mido.MidiFile(midi_filepath)`:
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


""" Tips

## Turn off Notes

In many cases, a note is turned off not by a `note_off` message,
but by a `note_on` message with `velocity` 0:

```
    Message('note_on', channel=7, note=90, velocity=92, time=1),
    Message('note_on', channel=7, note=90, velocity=0, time=479),
```
 
"""

""" Ticks, Beats, Tempo, Quarter-note, and everything about Time

[Definitions]
    - BPM
        - beats per minute
    - tempo
        - μs per beat
        - use `bpm2tempo()` and `tempo2bpm()` in `mido` to convert between BPM and tempo
    - TPB
        - ticks per beat
    - `time` of Message in mido
        - Delta time in ticks. Must be an integer.
        - See more:
        - https://mido.readthedocs.io/en/stable/files/midi.html#about-the-time-attribute

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

""" [Data Structure of Converted Dataframe of Notes]
columns:
    note, track, channel, instrument, velocity, start_time, end_time, duration, key
metadata:
    BPM
"""


class MidiToNotesDataframe:
    def __init__(self, midi_filepath):
        self.midi_filepath = midi_filepath
        self.mf = mido.MidiFile(self.midi_filepath)

    def parse_messages_by_types(self):
        message_types = [
            "note_on",
            "control_change",
            "program_change",
        ]
        meta_message_types = [
            "time_signature",
            "key_signature",
            "midi_port",
            "set_tempo",
            "end_of_track",
        ]
        for track in self.mf.tracks:
            for message in track:
                if message.type not in message_types + meta_message_types:
                    print(message)

    def run(self):
        # mf = self.mf
        # print(mf)
        self.parse_messages_by_types()
