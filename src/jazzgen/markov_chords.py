"""Chord progression Markov model."""
from __future__ import annotations

import json
import pickle
import random
from pathlib import Path
from typing import Dict, List, Tuple

from .chord_theory import ROOT_MAP, CANONICAL, transpose

Chord = Tuple[str, str]


def build_transition_matrix(
    corpus: Dict[str, List[List[Chord]]]
) -> Dict[Chord, Dict[Chord, float]]:
    """Build a first-order transition matrix from a chord corpus."""
    counts: Dict[Chord, Dict[Chord, int]] = {}
    for song in corpus.values():
        for bar in song:
            prev: Chord | None = None
            for chord in bar:
                chord_t: Chord = tuple(chord)  # JSON loads lists; convert to tuple
                if prev is not None:
                    counts.setdefault(prev, {}).setdefault(chord_t, 0)
                    counts[prev][chord_t] += 1
                prev = chord_t
    matrix: Dict[Chord, Dict[Chord, float]] = {}
    for prev, dests in counts.items():
        total = sum(dests.values())
        matrix[prev] = {ch: n / total for ch, n in dests.items()}
    return matrix


def save_matrix(matrix: Dict[Chord, Dict[Chord, float]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as fh:
        pickle.dump(matrix, fh)


def load_matrix(path: Path) -> Dict[Chord, Dict[Chord, float]]:
    with path.open("rb") as fh:
        return pickle.load(fh)


def load_corpus(path: Path) -> Dict[str, List[List[Chord]]]:
    with path.open() as fh:
        return json.load(fh)


def sample_progression(
    matrix: Dict[Chord, Dict[Chord, float]],
    bars: int = 12,
    key: str = "C",
    harmonic_rhythm: int = 1,
    seed: int | None = None,
) -> List[Chord]:
    """Sample a chord progression from the transition matrix."""
    rng = random.Random(seed)
    states = list(matrix.keys())
    current = rng.choice(states)
    steps = ROOT_MAP[key]
    progression: List[Chord] = []
    for _ in range(bars * harmonic_rhythm):
        progression.append((transpose(current[0], steps), current[1]))
        dests = matrix.get(current)
        if not dests:
            current = rng.choice(states)
        else:
            chords, weights = zip(*dests.items())
            current = rng.choices(chords, weights=weights, k=1)[0]
    return progression
