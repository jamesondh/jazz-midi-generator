"""Simple MIDI writer for chords and melody."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Tuple

import pretty_midi

from .chord_theory import ROOT_MAP

Chord = Tuple[str, str]
Event = Tuple[int, float, float]


def _chord_pitches(chord: Chord) -> List[int]:
    root, quality = chord
    root_midi = 60 + ROOT_MAP[root]
    if "m" in quality and not quality.startswith("maj"):
        third = root_midi + 3
    else:
        third = root_midi + 4
    seventh = root_midi + 10 if "7" in quality else root_midi + 11
    return [root_midi, third, seventh]


def write(
    chords: Iterable[Chord],
    melody: Iterable[Event],
    tempo: int,
    outfile: str | Path,
) -> None:
    """Write chords and melody to a MIDI file."""
    beat_sec = 60.0 / tempo
    pm = pretty_midi.PrettyMIDI(initial_tempo=tempo)
    comp = pretty_midi.Instrument(program=0)
    lead = pretty_midi.Instrument(program=0)
    beat = 0.0
    for chord in chords:
        pitches = _chord_pitches(chord)
        start = beat * beat_sec
        end = (beat + 1.0) * beat_sec
        for p in pitches:
            comp.notes.append(
                pretty_midi.Note(start=start, end=end, pitch=p, velocity=60)
            )
        beat += 1.0
    for pitch, start, end in melody:
        lead.notes.append(
            pretty_midi.Note(
                start=start * beat_sec, end=end * beat_sec, pitch=pitch, velocity=90
            )
        )
    pm.instruments.append(comp)
    pm.instruments.append(lead)
    pm.write(str(outfile))
