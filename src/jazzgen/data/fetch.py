"""Download raw datasets and compute checksums."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlretrieve

# URLs for the two primary datasets
DATASETS = {
    "jazzstandards": (
        "https://codeload.github.com/mikeoliphant/JazzStandards/zip/main",
        "JazzStandards.zip",
    ),
    "wjazzd": (
        "https://jazzomat.hfm-weimar.de/downloads/WJazzD/WJazzD_v2.0.zip",
        "WJazzD_v2.0.zip",
    ),
}

# Repository root resolved from this file location: fetch.py -> data -> jazzgen -> src -> repo
RAW_DIR = Path(__file__).resolve().parents[3] / "data" / "raw"
CHECKSUM_FILE = RAW_DIR / "checksums.json"


def sha256(path: Path) -> str:
    """Compute SHA-256 checksum for a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str, dest: Path) -> bool:
    """Download ``url`` to ``dest``. Returns True on success."""
    print(f"Downloading {url} -> {dest}")
    try:
        urlretrieve(url, dest)
        return True
    except (URLError, OSError) as exc:
        print(f"Failed to download {url}: {exc}")
        return False


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    checksums = {}

    for name, (url, fname) in DATASETS.items():
        filename = RAW_DIR / fname
        if fetch(url, filename):
            checksums[fname] = sha256(filename)

    with CHECKSUM_FILE.open("w") as fh:
        json.dump(checksums, fh, indent=2)
    print(f"Checksums written to {CHECKSUM_FILE}")


if __name__ == "__main__":
    main()
