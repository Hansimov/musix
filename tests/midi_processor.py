import mido
mid = mido.MidiFile("./mids/passionate-duelist.mid")

# General MIDI Program Chart
#   https://jazz-soft.net/demo/GeneralMidi.html

for msg in mid:
    if msg.type == 'program_change':
        print(msg)