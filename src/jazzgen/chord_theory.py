"""Basic chord theory helpers and look-up tables."""
from __future__ import annotations

from typing import Dict, List, Tuple

ROOTS = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
ROOT_MAP = {name: i for i, name in enumerate(ROOTS)}
CANONICAL = {i: name for i, name in enumerate(ROOTS)}

# Simple diatonic scale degrees per common chord quality
SCALE_DEGREES: Dict[str, List[int]] = {
    "maj7": [0, 2, 4, 5, 7, 9, 11],
    "m7": [0, 2, 3, 5, 7, 9, 10],
    "7": [0, 2, 4, 5, 7, 9, 10],
    "m7b5": [0, 2, 3, 5, 6, 8, 10],
}

# Allowed color tones relative to chord root
COLOR_TONES: Dict[str, List[int]] = {
    "maj7": [9, 13],
    "7": [9, 13],
    "m7": [9, 11],
    "m7b5": [11],
}


def transpose(root: str, steps: int) -> str:
    idx = ROOT_MAP[root]
    return CANONICAL[(idx + steps) % 12]


def tritone_substitution(root: str) -> str:
    """Return the root a tritone away from ``root``."""
    return transpose(root, 6)


def secondary_dominant(target_root: str) -> str:
    """Return the V of the given ``target_root``."""
    return transpose(target_root, 7)
