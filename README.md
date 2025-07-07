# Jazz MIDI Generator

This project automatically generates a jazz chord progression and melodic line and exports the result to a MIDI file.  It is implemented as a headless Python package.

## Quick start

1. Install dependencies (Python 3.10+ recommended):

```bash
pip install music21 pretty_midi mido numpy pyyaml click pytest
```

2. Install the package locally so the `jazzgen` module resolves.  Editable
   installs require a recent version of `pip` and `setuptools` (23.1+).  If you
   encounter an error, upgrade first and then install:

```bash
python -m pip install --upgrade pip setuptools
python -m pip install -e .
```

3. (Optional) fetch the raw datasets if you need fresh copies. A small subset
   is already included under `data/raw` so you can skip this step:

```bash
python -m jazzgen.data.fetch
```

4. Build the processed chord corpus.  This only needs to be done once:

```bash
python -m jazzgen.data.build_chord_corpus
```

5. Train the chord model:

```bash
python scripts/train_chord_markov.py
```

6. Generate a MIDI file:

```bash
python -m jazzgen.cli --key C --bars 12 --tempo 200 output.mid
```

