"""Generation pipeline."""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from . import markov_chords

Chord = Tuple[str, str]


def generate(
    seed: int = 42,
    key: str = "C",
    bars: int = 12,
    tempo: int = 200,
    outfile: str | None = None,
    matrix_path: str | Path | None = None,
) -> List[Chord]:
    """Generate a chord progression.

    This is a minimal skeleton. Melody and MIDI output will be implemented later.
    If ``outfile`` is given, a text representation of the chords is written to
    that path.
    """
    repo_root = Path(__file__).resolve().parents[2]
    if matrix_path is None:
        matrix_path = repo_root / "data" / "processed" / "chord_transitions.pkl"
    else:
        matrix_path = Path(matrix_path)
    if not matrix_path.exists():
        raise FileNotFoundError(matrix_path)
    matrix = markov_chords.load_matrix(matrix_path)
    chords = markov_chords.sample_progression(
        matrix, bars=bars, key=key, seed=seed
    )
    if outfile:
        Path(outfile).write_text(" ".join(f"{r}{q}" for r, q in chords))
    return chords

