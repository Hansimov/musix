# from manim import MovingCameraScene
import pandas as pd

from collections import Counter
from pathlib import Path
from utils.midi_parser import MidiParser


class OnlyMyRailgun:
    # https://musescore.com/user/10087681/scores/3130296
    midi_filepath = (
        Path(__file__).parents[1] / "mids" / "Only_My_Railgun_liyifei1218.mid"
    )

    def run(self):
        mp = MidiParser(self.midi_filepath)
        mp.run()


if __name__ == "__main__":
    only_my_railgun = OnlyMyRailgun()
    only_my_railgun.run()
