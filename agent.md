# Development status

Data fetching and corpus parsing have been implemented (section 1 of the plan).\
This includes iRealPro chord extraction and a basic MIDI solo event parser.\
Chord Markov training and progression sampling are now functional (`train_chord_markov.py` and `markov_chords.py`).
A minimal generation pipeline and CLI are now available (`pipeline.py` and `cli.py`).
Basic rhythm pattern utilities and a note-choice helper have been added (`rhythm_patterns.py`, `note_choice.py`, `rhythm_engine.py`).
An initial grammar-driven melody engine now composes short phrases (`melody_grammar.py`, `melody_engine.py`) and a MIDI writer exports the result (`midi_writer.py`). The pipeline and CLI have been updated to produce MIDI files.

## Next steps

- Expand the grammar and improve note selection heuristics.
