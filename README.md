# Jazz MIDI Generator

This project automatically generates a jazz chord progression and melodic line and exports the result to a MIDI file.  It is implemented as a headless Python package.

## Quick start

1. Install dependencies (Python 3.10+ recommended):

```bash
pip install music21 pretty_midi mido numpy pyyaml click pytest
```

2. Fetch raw datasets:

```bash
python -m jazzgen.data.fetch
```

3. (Later) Train the models and generate MIDI with the CLI.

