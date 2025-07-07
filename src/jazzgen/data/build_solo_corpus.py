"""Parse WJazzD MIDI files into a simple note event table."""
from __future__ import annotations

from pathlib import Path
import io
import json
import zipfile

import pretty_midi


def parse_midi(data: bytes) -> list[dict]:
    """Return a list of note events from MIDI bytes."""
    midi = pretty_midi.PrettyMIDI(io.BytesIO(data))
    events = []
    prev_pitch = None
    for instrument in midi.instruments:
        if instrument.is_drum:
            continue
        for note in instrument.notes:
            if prev_pitch is None:
                interval = 0
            else:
                interval = note.pitch - prev_pitch
            events.append({
                "start": note.start,
                "pitch": note.pitch,
                "interval": interval,
            })
            prev_pitch = note.pitch
    return events


def build_corpus(zip_path: Path, out_path: Path) -> None:
    out: dict[str, list[dict]] = {}
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if not name.lower().endswith('.mid'):
                continue
            with zf.open(name) as fh:
                data = fh.read()
            events = parse_midi(data)
            out[name] = events
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open('w') as fh:
        json.dump(out, fh)
    print(f"Wrote {out_path}")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    zip_path = repo_root / 'data' / 'raw' / 'RELEASE2.0_mid_unquant.zip'
    out_path = repo_root / 'data' / 'processed' / 'solo_corpus.json'
    build_corpus(zip_path, out_path)


if __name__ == '__main__':
    main()
