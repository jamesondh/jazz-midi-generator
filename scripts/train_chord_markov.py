"""Train chord transition matrix from processed corpus."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jazzgen.markov_chords import build_transition_matrix, save_matrix


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true", help="overwrite existing output")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    corpus_path = repo_root / "data" / "processed" / "chord_corpus.json"
    out_path = repo_root / "data" / "processed" / "chord_transitions.pkl"

    if out_path.exists() and not args.rebuild:
        print(f"{out_path} already exists. Use --rebuild to regenerate.")
        return

    with corpus_path.open() as fh:
        corpus = json.load(fh)
    matrix = build_transition_matrix(corpus)
    save_matrix(matrix, out_path)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
