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

    tempo = 500000  (by default)
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
    note, port, track, channel, instrument, velocity, start_time, end_time, duration, key
metadata:
    BPM
"""


"""
* Some utils implementations in mido:
    * https://github.com/mido/mido/blob/main/mido/midifiles/units.py
* MIDI File Format: Tempo and Timebase
    * http://midi.teragonaudio.com/tech/midifile/ppqn.htm
"""


def tick2second(tick, tempo, ticks_per_beat) -> float:
    return tick * tempo * 1e-6 / ticks_per_beat


def second2tick(second, tempo, ticks_per_beat) -> int:
    return int(second * ticks_per_beat * 1e6 / tempo)


def bpm2tempo(bpm, denominator=4) -> int:
    return int(60 * 1e6 * denominator / (4 * bpm))


def tempo2bpm(tempo, denominator=4) -> float:
    return 60 * 1e6 * denominator / (4 * tempo)


class Note:
    def __init__(self):
        pass

    def create(self):
        note_attrs = [
            "note",
            "port",
            "track",
            "channel",
            "instrument",
            "velocity",
            "start_time",
            "duration",
            "key",
        ]


class MidiParser:
    def __init__(self, midi_filepath):
        self.mf = mido.MidiFile(midi_filepath)
        self.ticks = 0
        self.tracks = []
        self.notes = []

        self.map_message_functions_by_types()

    def set_header_attrs(self):
        """
        * Standard MIDI Files — Mido 1.3.0 documentation
            * https://mido.readthedocs.io/en/stable/files/midi.html#meta-messages
        """
        mf_attrs = ["filename", "type", "length", "ticks_per_beat"]
        for attr in mf_attrs:
            setattr(self, attr, getattr(self.mf, attr))

    def map_message_functions_by_types(self):
        self.message_type_funcs = {
            "note_on": self.process_note,
            "note_off": self.process_note,
            "control_change": self.change_control,
            "program_change": self.change_program,
        }
        self.meta_message_type_funcs = {
            "time_signature": self.set_time_signature,
            "key_signature": self.set_key_signature,
            "midi_port": self.set_midi_port,
            "set_tempo": self.set_tempo,
            "end_of_track": self.set_end_of_track,
        }

    def set_track_meta(self, keys, message, value_type=int):
        if type(keys) is not list:
            keys = [keys]

        for key in keys:
            val = value_type(getattr(message, key))
            setattr(self, key, val)
            print(val, end=" ")

    def set_time_signature(self, message):
        """
        MetaMessage('time_signature',
            numerator=4,
            denominator=4,
            clocks_per_click=24,
            notated_32nd_notes_per_beat=8,
            time=0,
        )

        https://mido.readthedocs.io/en/stable/meta_message_types.html#time-signature-0x58

        * MIDI File Format: Time Signature
            * http://midi.teragonaudio.com/tech/midifile/time.htm
        * What is notated_32nd_notes_per_beat
            * https://www.midi.org/forum/5045-what-is-notated_32nd_notes_per_beat
        """
        time_signature_keys = [
            "numerator",
            "denominator",
            "clocks_per_click",
            "notated_32nd_notes_per_beat",
        ]
        self.set_track_meta(time_signature_keys, message)

    def set_key_signature(self, message):
        """
        MetaMessage('key_signature',
            key='C',
            time=0,
        )
        https://mido.readthedocs.io/en/stable/meta_message_types.html#key-signature-0x59
        """
        self.set_track_meta("key", message, value_type=str)

    def set_midi_port(self, message):
        """
        MetaMessage('midi_port',
            port=0,
            time=0,
        )

        https://mido.readthedocs.io/en/stable/meta_message_types.html#midi-port-0x21
        """
        self.set_track_meta("port", message)

    def set_tempo(self, message):
        """
        MetaMessage('set_tempo',
            tempo=500000,
            time=0,
        )

        tempo: μs per beat, default value is: 500000

        https://mido.readthedocs.io/en/stable/meta_message_types.html#set-tempo-0x51
        """
        self.set_track_meta("tempo", message)
        self.bpm = tempo2bpm(
            self.tempo,
            denominator=self.denominator,
        )

    def set_end_of_track(self, message):
        """
        MetaMessage('end_of_track',
            time=1
        )
        https://mido.readthedocs.io/en/stable/meta_message_types.html#end-of-track-0x2f
        """
        self.set_track_meta([], message)

    def process_note(self, message):
        note_keys = ["note", "channel", "velocity"]
        if message.type == "note_on" and message.velocity > 0:
            note_dict = {}
            note_dict["start_tick"] = self.ticks
            for key in note_keys:
                note_dict[key] = getattr(message, key)
            self.notes.append(note_dict)
        elif message.type == "note_off" or message.velocity == 0:
            note_dict = self.notes[-1]
            note_dict["play_ticks"] = message.time
            note_dict["end_tick"] = note_dict["start_tick"] + message.time
            self.notes[-1] = note_dict
            print(f"  > Note: {self.notes[-1]}")
        else:
            raise Exception(f"Error when parsing: {message}")

    def change_control(self, message):
        pass

    def change_program(self, message):
        pass

    def parse_message(self, message):
        if not hasattr(self, "tempo"):
            print(f"{self.ticks}: {message}")
        else:
            seconds = round(tick2second(self.ticks, self.tempo, self.ticks_per_beat), 1)
            print(f"{seconds}: {message}")

        if message.type in self.meta_message_type_funcs.keys():
            self.meta_message_type_funcs[message.type](message)
            self.ticks += message.time
        elif message.type in self.message_type_funcs.keys():
            self.message_type_funcs[message.type](message)
            self.ticks += message.time
        else:
            raise Exception(f"Unknown message type: {message.type}")

    def parse_track(self, track):
        for message in track:
            self.parse_message(message)

    def parse_tracks(self):
        for track in self.mf.tracks:
            self.ticks = 0
            self.parse_track(track)

    def run(self):
        self.set_header_attrs()
        self.parse_tracks()
