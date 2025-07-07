"""Rhythm pattern utilities."""
from __future__ import annotations

import random
from pathlib import Path
from typing import List

import yaml

# Default embedded patterns used if YAML not found
DEFAULT_PATTERNS = {
    "swing": ["q,8,8,8,8,q", "8,8,8,8,8,8,8,8"],
    "straight": ["q,q,q,q"],
}


def _load_patterns(style: str) -> List[str]:
    repo_root = Path(__file__).resolve().parents[2]
    path = repo_root / "data" / "patterns" / f"{style}.yaml"
    if path.exists():
        with path.open() as fh:
            doc = yaml.safe_load(fh)
            if isinstance(doc, list):
                return doc
    return DEFAULT_PATTERNS.get(style, DEFAULT_PATTERNS["swing"])


_DURATION_MAP = {"q": 1.0, "h": 2.0, "w": 4.0, "8": 0.5, "16": 0.25}


def _parse(pattern: str) -> List[float]:
    return [_DURATION_MAP.get(tok.strip(), 1.0) for tok in pattern.split(",")]


def choose_pattern(style: str = "swing", rng: random.Random | None = None) -> List[float]:
    """Return a list of beat durations for one bar of the given style."""
    rng = rng or random
    patterns = _load_patterns(style)
    pattern = rng.choice(patterns)
    return _parse(pattern)
