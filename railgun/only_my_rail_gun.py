# from manim import MovingCameraScene
from collections import Counter
from pathlib import Path
import mido
import librosa
import pandas as pd


class OnlyMyRailGun:
    # https://musescore.com/user/10087681/scores/3130296
    midi_filepath = (
        Path(__file__).parents[1] / "mids" / "Only_My_Railgun_liyifei1218.mid"
    )

    def run(self):
        mf = mido.MidiFile(self.midi_filepath)
        notes = []
        for msg in mf:
            if msg.type == "note_on" or msg.type == "note_off":
                note = msg.note
                velocity = msg.velocity
                time = msg.time
                type = msg.type
                notes.append([note, velocity, time, type])

        df = pd.DataFrame(notes, columns=["note", "velocity", "time", "type"])
        df = df.sort_values(by="time")
        print(df)


if __name__ == "__main__":
    only_my_railgun = OnlyMyRailGun()
    only_my_railgun.run()
