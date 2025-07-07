from jazzgen.pipeline import generate
import pickle
from pathlib import Path


def test_generate(tmp_path: Path) -> None:
    matrix = {("C", "7"): {("F", "7"): 1.0}, ("F", "7"): {("C", "7"): 1.0}}
    pkl = tmp_path / "m.pkl"
    with pkl.open("wb") as fh:
        pickle.dump(matrix, fh)
    out = tmp_path / "gen.mid"
    chords = generate(key="C", bars=2, seed=123, matrix_path=pkl, outfile=out)
    assert len(chords) == 2
    assert all(len(ch) == 2 for ch in chords)
    assert out.exists()
