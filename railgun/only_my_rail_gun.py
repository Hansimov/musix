# from manim import MovingCameraScene
from pathlib import Path
import mido
from collections import Counter


class OnlyMyRailGun:
    # https://musescore.com/user/10087681/scores/3130296
    midi_filepath = (
        Path(__file__).parents[1] / "mids" / "Only_My_Railgun_liyifei1218.mid"
    )

    def run(self):
        mf = mido.MidiFile(self.midi_filepath)
        note_counts = Counter()
        for i, track in enumerate(mf.tracks):
            # print(f"Track {i}: {track.name}")
            for msg in track:
                if msg.type == "note_on":
                    channel = msg.channel
                    note_counts[channel] += 1
                    # print(msg)
        for channel, count in note_counts.most_common():
            print(f"Channel {channel}: {count} notes")


if __name__ == "__main__":
    only_my_railgun = OnlyMyRailGun()
    only_my_railgun.run()
