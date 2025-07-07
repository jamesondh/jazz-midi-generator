"""Command line interface for jazzgen."""
from __future__ import annotations

import click

from . import pipeline


@click.command()
@click.option("--key", default="C", help="Key signature")
@click.option("--bars", default=12, type=int, help="Number of bars")
@click.option("--seed", default=42, type=int, help="Random seed")
@click.option("--tempo", default=200, type=int, help="Tempo in BPM")
@click.argument("outfile", required=False)
def main(key: str, bars: int, seed: int, tempo: int, outfile: str | None) -> None:
    """Generate a chord progression and MIDI file."""
    chords = pipeline.generate(
        key=key, bars=bars, seed=seed, tempo=tempo, outfile=outfile
    )
    click.echo(" ".join(f"{r}{q}" for r, q in chords))


if __name__ == "__main__":
    main()
