"""Convert duration patterns to start/stop times."""
from __future__ import annotations

from typing import Iterable, List, Tuple


def quantise(durations: Iterable[float], swing_ratio: float = 0.66) -> List[Tuple[float, float]]:
    """Return list of (start, end) beat positions applying swing."""
    times: List[Tuple[float, float]] = []
    t = 0.0
    for dur in durations:
        start = t
        end = t + dur
        if swing_ratio != 0 and dur == 0.5:
            # apply swing on pairs of eighth notes
            if int(t * 2) % 2 == 0:
                end = start + dur * swing_ratio
            else:
                start = end - dur * swing_ratio
        times.append((start, end))
        t += dur
    return times
