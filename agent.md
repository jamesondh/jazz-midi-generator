# Development status

Data fetching and corpus parsing have been implemented (section 1 of the plan).\
This includes iRealPro chord extraction and a basic MIDI solo event parser.

## Next steps

- Train a Markov model from the parsed chord corpus (`scripts/train_chord_markov.py`).
- Implement chord progression sampling (`markov_chords.py`).
- Continue with melody/rhythm modules and CLI as outlined in `IMPLEMENTATION_PLAN.md`.
