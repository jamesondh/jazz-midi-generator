"""Very small melody composition stub."""
from __future__ import annotations

import random
from typing import List, Sequence, Tuple

from .note_choice import pick_pitch
from .rhythm_patterns import choose_pattern
from .rhythm_engine import quantise
from .melody_grammar import expand

Chord = Tuple[str, str]


def compose(
    chords: Sequence[Chord],
    seed: int = 42,
    style: str = "swing",
) -> List[Tuple[int, float, float]]:
    """Return list of (pitch, start, end) events."""
    rng = random.Random(seed)
    events: List[Tuple[int, float, float]] = []
    beat_pos = 0.0
    last_pitch: int | None = None
    for chord in chords:
        pattern = choose_pattern(style, rng)
        times = quantise(pattern)
        for dur, (start, end) in zip(pattern, times):
            symbol = expand("PHRASE", rng)[0]
            if symbol == "REST":
                last_pitch = None
                continue
            pitch = pick_pitch(chord, last_pitch, rng=rng)
            events.append((pitch, beat_pos + start, beat_pos + end))
            last_pitch = pitch
        beat_pos += sum(pattern)
    return events
