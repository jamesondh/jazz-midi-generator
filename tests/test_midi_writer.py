import pretty_midi
from pathlib import Path

from jazzgen.midi_writer import write


def test_write(tmp_path: Path) -> None:
    chords = [("C", "7"), ("F", "7")]
    melody = [(60, 0.0, 1.0), (62, 1.0, 2.0)]
    out = tmp_path / "out.mid"
    write(chords, melody, tempo=120, outfile=out)
    pm = pretty_midi.PrettyMIDI(str(out))
    assert len(pm.instruments) >= 2
    assert out.exists()
