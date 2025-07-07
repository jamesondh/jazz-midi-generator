"""Command line interface for jazzgen."""
from __future__ import annotations

import click

from . import pipeline


@click.command()
@click.option("--key", default="C", help="Key signature")
@click.option("--bars", default=12, type=int, help="Number of bars")
@click.option("--seed", default=42, type=int, help="Random seed")
@click.argument("outfile", required=False)
def main(key: str, bars: int, seed: int, outfile: str | None) -> None:
    """Generate a chord progression and optionally write to ``outfile``."""
    chords = pipeline.generate(key=key, bars=bars, seed=seed, outfile=outfile)
    click.echo(" ".join(f"{r}{q}" for r, q in chords))


if __name__ == "__main__":
    main()
