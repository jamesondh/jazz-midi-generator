"""Stochastic grammar for melody generation."""
from __future__ import annotations

import random
from typing import List

# Simple grammar mapping symbols to weighted productions
GRAMMAR = {
    "BAR": [("PHRASE", 1.0)],
    "PHRASE": [("RUN", 0.6), ("ENCLOSURE", 0.3), ("REST", 0.1)],
    "RUN": [("SCALE_STEP", 0.7), ("LEAP", 0.3)],
    "ENCLOSURE": [("LEAP", 0.5), ("SCALE_STEP", 0.5)],
    "SCALE_STEP": [("NOTE", 1.0)],
    "LEAP": [("NOTE", 1.0)],
    "REST": [("REST", 1.0)],
    "NOTE": [],
}

TERMINALS = {"NOTE", "REST"}


def expand(symbol: str, rng: random.Random) -> List[str]:
    """Recursively expand ``symbol`` and return a list of terminals."""
    if symbol in TERMINALS or symbol not in GRAMMAR:
        return [symbol]
    productions = GRAMMAR[symbol]
    choices, weights = zip(*productions)
    next_sym = rng.choices(choices, weights=weights, k=1)[0]
    return expand(next_sym, rng)
