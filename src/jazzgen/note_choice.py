"""Simple note choice logic."""
from __future__ import annotations

import random
from typing import Dict, Tuple

from . import chord_theory

Chord = Tuple[str, str]


CATEGORY_WEIGHTS: Dict[str, Dict[str, float]] = {
    "default": {"chord": 0.7, "color": 0.2, "approach": 0.1},
}


def pick_pitch(
    chord: Chord,
    last_pitch: int | None,
    weights: Dict[str, float] | None = None,
    approach_cache: Dict[str, int] | None = None,
    rng: random.Random | None = None,
) -> int:
    """Return a MIDI pitch for the given chord."""
    rng = rng or random
    w = weights or CATEGORY_WEIGHTS["default"]
    root, quality = chord
    degrees = chord_theory.SCALE_DEGREES.get(quality, chord_theory.SCALE_DEGREES["maj7"])
    root_midi = 60 + chord_theory.ROOT_MAP[root]
    choice = rng.choices(
        ["chord", "color"],
        weights=[w.get("chord", 1.0), w.get("color", 1.0)],
        k=1,
    )[0]
    if choice == "color":
        allowed = chord_theory.COLOR_TONES.get(quality, [9])
        degree = rng.choice(allowed)
    else:
        degree = rng.choice(degrees)
    return root_midi + degree
