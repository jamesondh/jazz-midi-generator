# Development status

Data fetching and corpus parsing have been implemented (section 1 of the plan).\
This includes iRealPro chord extraction and a basic MIDI solo event parser.\
Chord Markov training and progression sampling are now functional (`train_chord_markov.py` and `markov_chords.py`).
A minimal generation pipeline and CLI are now available (`pipeline.py` and `cli.py`).
Basic rhythm pattern utilities and a note-choice helper have been added (`rhythm_patterns.py`, `note_choice.py`, `rhythm_engine.py`).
An initial grammar-driven melody engine now composes short phrases (`melody_grammar.py`, `melody_engine.py`) and a MIDI writer exports the result (`midi_writer.py`). The pipeline and CLI have been updated to produce MIDI files.
The README now documents a working quick-start workflow including package installation and dataset preparation.

## Next steps

- The MIDI writer and integration tests from step 7 are complete.
- Continue with step 8 of the plan: polish documentation and do a listening
  review.
- Updated README with a step to build the chord corpus before training.
- Add a golden-file regression test that checks a fixed seed produces the same
  MIDI hash.
- Insert an architecture diagram and CLI options table into the README.
- Manually audition a 32-bar solo in B-flat to confirm there are no glaring
  rhythmic glitches.
