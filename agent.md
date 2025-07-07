# Development status

Data fetching and corpus parsing have been implemented (section 1 of the plan).\
This includes iRealPro chord extraction and a basic MIDI solo event parser.\
Chord Markov training and progression sampling are now functional (`train_chord_markov.py` and `markov_chords.py`).
A minimal generation pipeline and CLI are now available (`pipeline.py` and `cli.py`).

## Next steps

- Implement rhythm and melody modules as described in `IMPLEMENTATION_PLAN.md`.
