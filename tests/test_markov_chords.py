from jazzgen.markov_chords import build_transition_matrix, sample_progression


def test_markov_sample():
    corpus = {
        "song": [[("C", "7"), ("F", "7")], [("Bb", "7")]]
    }
    matrix = build_transition_matrix(corpus)
    assert ("C", "7") in matrix
    prog = sample_progression(matrix, bars=2, key="C", seed=123)
    assert len(prog) == 2
    assert all(len(ch) == 2 for ch in prog)
