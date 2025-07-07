"""Parse iRealPro chord dataset and store processed corpus."""
from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

ROOT_MAP = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
}
CANONICAL = {
    0: "C",
    1: "Db",
    2: "D",
    3: "Eb",
    4: "E",
    5: "F",
    6: "Gb",
    7: "G",
    8: "Ab",
    9: "A",
    10: "Bb",
    11: "B",
}


RE_CHORD = re.compile(r"^([A-G][b#]?)(.*)$")


def parse_symbol(symbol: str) -> tuple[str, str]:
    """Return ``(root, quality)`` from chord symbol like ``G7alt``."""
    m = RE_CHORD.match(symbol.strip())
    if not m:
        raise ValueError(f"Invalid chord symbol: {symbol}")
    root, quality = m.groups()
    return root, quality or ""


def transpose_root(root: str, steps: int) -> str:
    val = ROOT_MAP[root]
    new_val = (val + steps) % 12
    return CANONICAL[new_val]


def parse_song(song: dict) -> list[list[tuple[str, str]]]:
    key = song.get("Key", "C")
    steps = (0 - ROOT_MAP.get(key, 0)) % 12
    corpus: list[list[tuple[str, str]]] = []
    for section in song.get("Sections", []):
        seg = section.get("MainSegment", {})
        chords_str = seg.get("Chords", "")
        for bar in chords_str.split("|"):
            bar_chords = []
            for sym in filter(None, bar.split(",")):
                root, qual = parse_symbol(sym)
                root = transpose_root(root, steps)
                bar_chords.append((root, qual))
            if bar_chords:
                corpus.append(bar_chords)
    return corpus


def build_corpus(zip_path: Path, out_path: Path) -> None:
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open("JazzStandards-main/JazzStandards.json") as fh:
            data = json.load(fh)
    out = {song["Title"]: parse_song(song) for song in data}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as fh:
        json.dump(out, fh, indent=2)
    print(f"Wrote {out_path}")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    zip_path = repo_root / "data" / "raw" / "JazzStandards.zip"
    out_path = repo_root / "data" / "processed" / "chord_corpus.json"
    build_corpus(zip_path, out_path)


if __name__ == "__main__":
    main()
