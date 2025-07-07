# Development status

Data fetching and corpus parsing have been implemented (section 1 of the plan).\
This includes iRealPro chord extraction and a basic MIDI solo event parser.\
Chord Markov training and progression sampling are now functional (`train_chord_markov.py` and `markov_chords.py`).
A minimal generation pipeline and CLI are now available (`pipeline.py` and `cli.py`).
Basic rhythm pattern utilities and a note-choice helper have been added (`rhythm_patterns.py`, `note_choice.py`, `rhythm_engine.py`).

## Next steps

- Integrate grammar-based melody generation and write MIDI output.
