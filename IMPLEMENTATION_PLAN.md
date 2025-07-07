# `jazz-midi-generator` Implementation Plan

Below is a **step‑by‑step implementation plan** for a minimal, head‑less Python tool that automatically generates

- (1) a jazz chord progression and
- (2) a stylistically‑controlled melody/solo line over that progression

and writes the result to a single `.mid` file.

---

## 0  Project Skeleton & Environment

| Folder                     | Purpose                                                           |
| -------------------------- | ----------------------------------------------------------------- |
| `/src`                     | Python packages and modules (see §2)                              |
| `/data/raw`                | Un‑modified external datasets (MIDI, JSON, SQL)                   |
| `/data/processed`          | Pickled or JSON artefacts (Markov tables, grammars, lick library) |
| `/notebooks`               | One‑off analysis / inspection (optional)                          |
| `/tests`                   | PyTest unit + integration tests                                   |
| `setup.cfg/pyproject.toml` | Package metadata & black/isort/my‑py lint settings                |
| `README.md`                | Quick‑start + CLI usage                                           |

**Python 3.10+** recommended.

### Dependencies

```bash
pip install music21 pretty_midi mido numpy pyyaml click pytest
```

- **music21** – symbolic music objects & theory helpers([music21.org][1])
- **pretty_midi / mido** – fast MIDI read/write/inspection([pypi.org][2])
- **numpy / pyyaml / click / pytest** – numerics, configs, CLI, tests

---

## 1  Data Acquisition & Pre‑processing

| Resource                                                                                                   | What we need                                        | Notes                                            |
| ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------ |
| **Jazz Standards / iRealPro** playlist dump (JSON)([github.com][3])                                        | Chord charts for \~1 300 tunes                      | Already JSON; no audio; OK for Markov on chords. |
| **Weimar Jazz Database (WJazzD)** – un‑quantised MIDI solos + SQLite metadata([jazzomat.hfm-weimar.de][4]) | \~450 professional solos with aligned chord symbols | ODbL licence—retain attribution.                 |
| Any personal MIDI / MusicXML leadsheets                                                                    | Optional extra style material                       | Keep licensing in mind.                          |

### 1.1  Automated fetch script (`src/data/fetch.py`)

- Download archives to `/data/raw`.
- Compute SHA‑256 and store in `checksums.json` for reproducibility.

### 1.2  Chord‑progression corpus builder (`src/data/build_chord_corpus.py`)

1. Parse every song in the iRealPro JSON.
2. Normalise symbols → `(root, quality)` tuples (e.g. **G7alt** → `("G", "7alt")`).
3. Transpose to **concert C** to reduce state‑space.
4. Store each tune as an array of bars with chord‑per‑beat resolution.

### 1.3  Solo corpus builder (`src/data/build_solo_corpus.py`)

1. Traverse WJazzD MIDI; load with `pretty_midi`.
2. Use metadata or heuristic down‑beat detection to align notes to chords.
3. For every note event compute:
   `beat_index`, `midi_pitch`, `interval_from_previous`, **tone‑category** relative to current chord (Chord / Color / Approach / Other).
4. Save to **Parquet** or Pickled Pandas for quick reload.

---

## 2  Core Python Modules

### 2.1 `chord_theory.py`

- Look‑up tables for:

  - Diatonic scales per chord quality
  - Valid **color tones** (9, 11, 13, etc.)
  - Tritone and secondary‑dominant substitution helpers

### 2.2 `markov_chords.py`

- Build **first‑ or second‑order transition matrix** from processed corpus.
- Provide `sample_progression(key, bars, style_cfg)` with knobs:

  - harmonic_rhythm (chords/bar)
  - substitution_probabilities
  - sectional_templates (12‑bar, 32‑bar, etc.)

### 2.3 `rhythm_patterns.py`

- YAML file per style: list of bar‑length **duration strings** (e.g. `"8,8,8,8,8,8,8,8"` or `"q, 8., 16, q"`).
- Function `choose_pattern(style)` returns list of (duration_in_beats).

### 2.4 `melody_grammar.py`

- **Lightweight stochastic grammar** implemented as nested Python dicts:

```python
GRAMMAR = {
    "BAR": [("PHRASE", 1.0)],
    "PHRASE": [("RUN", 0.6), ("ENCLOSURE", 0.3), ("REST", 0.1)],
    "RUN":    [("SCALE_STEP", 0.7), ("LEAP", 0.3)],
    ...
}
```

- Terminal generators delegate to `note_choice.py` (below).

### 2.5 `note_choice.py`

```python
def pick_pitch(chord, last_pitch, category_weights, approach_cache, rng):
    """
    1. Decide on category (Chord, Color, Approach, Rest)
    2. If Approach: store target in approach_cache
    3. Return midi_pitch
    """
```

- Ensures **chord tones on strong beats**; resolves pending approach tones.

### 2.6 `rhythm_engine.py`

- Turn a duration list plus tempo into absolute tick start/stop times.
- Optionally apply **swing** quantisation (`swing_ratio=0.66`).

### 2.7 `midi_writer.py`

- Convert chord list to separate piano‑comping track (simple root‑3rd‑7th voicing, optional).
- Dump melody into lead track.
- Save single‑file Standard MIDI 1.

### 2.8 `pipeline.py`

```python
def generate(seed=42,
             style="bebop",
             key="C",
             bars=32,
             tempo=200,
             outfile="output.mid"):
    chords = markov_chords.sample_progression(...)
    melody = melody_engine.compose(chords, style_cfg)
    midi_writer.write(chords, melody, tempo, outfile)
```

### 2.9 `cli.py`

```bash
python -m jazzgen.cli --style bebop --key F --tempo 240 --bars 32 out.mid
```

Uses `click` for arguments and passes through to `pipeline.generate`.

---

## 3  Model‑Building Steps

| Step                                           | Script                               | Output                                  |
| ---------------------------------------------- | ------------------------------------ | --------------------------------------- |
| _Train chord Markov_                           | `scripts/train_chord_markov.py`      | `/data/processed/chord_transitions.pkl` |
| _Derive tone‑category frequencies_ from WJazzD | `scripts/analyse_tone_categories.py` | `tone_weights.yaml` per style           |
| _Extract lick library_ (optional)              | `scripts/extract_licks.py`           | `lick_bank.json` keyed by cadence       |

All scripts should accept `--rebuild` flag and run in <2 min on a laptop.

---

## 4  Testing & Validation

| Layer       | Test                                                                                      |
| ----------- | ----------------------------------------------------------------------------------------- |
| Unit        | _Chord parsing_, _tone categorisation_, _duration parsing_                                |
| Property    | For every generated bar: verify ≤ range_limit and all strong‑beat tones ∈ allowed set     |
| Golden‑file | Seed = 123 should always regenerate **identical MIDI hash**                               |
| Listen      | Manual smoke test: generate a 32‑bar bebop solo in B♭ at 240 BPM, audition in any player. |

---

## 5  Documentation

- `README.md` quick‑start: install, train, generate.
- Doc‑strings in every public function.
- Architecture diagram (markdown ASCII OK).
- Table in README listing configurable style parameters and defaults.

---

## 6  Future Enhancements (non‑blocking)

1. **Motif development** – detect generated 2‑bar motif and transpose / sequence it.
2. **Interactive genetic post‑processing** – optional module that mutates melody and lets user thumbs‑up/down to evolve improvements (inspired by GenJam).
3. **External grammar import** – read Impro‑Visor `*.sty` to re‑use existing grammars([en.wikipedia.org][5]).

---

### Licensing & Compliance

- iRealPro JSON was scraped by the community and is redistributed under a permissive notice in the GitHub repo – retain the notice in `/THIRDPARTY.md`.([github.com][3])
- WJazzD is **ODbL** – credit “Jazzomat Research Project, Hochschule für Musik Franz Liszt Weimar”.([jazzomat.hfm-weimar.de][4])
- Generated MIDI files are yours; no dataset content is embedded verbatim.

---

### Implementation Plan

| Step | Milestone                                 |
| ---- | ----------------------------------------- |
| 1    | Environment setup, fetch & checksum data  |
| 2    | Chord corpus parser + Markov training     |
| 3    | Solo corpus parser + tone analysis        |
| 4    | Chord generator + CLI skeleton            |
| 5    | Rhythm + note‑choice engine               |
| 6    | Grammar layer + initial melody generation |
| 7    | MIDI writer + integration tests           |
| 8    | Polish, docs, empirical listening review  |

[1]: https://www.music21.org/music21docs/moduleReference/moduleChord.html?utm_source=chatgpt.com "Chord - music21 Documentation - Michael Scott Asato Cuthbert"
[2]: https://pypi.org/project/pretty_midi/?utm_source=chatgpt.com "pretty_midi - PyPI"
[3]: https://github.com/mikeoliphant/JazzStandards?utm_source=chatgpt.com "mikeoliphant/JazzStandards: Chord data for many jazz standards"
[4]: https://jazzomat.hfm-weimar.de/download/download.html?utm_source=chatgpt.com "Download - The Jazzomat Research Project - HfM Weimar"
[5]: https://en.wikipedia.org/wiki/Impro-Visor?utm_source=chatgpt.com "Impro-Visor"
