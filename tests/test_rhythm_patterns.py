from jazzgen.rhythm_patterns import choose_pattern


def test_choose_pattern():
    pat = choose_pattern("swing")
    assert isinstance(pat, list)
    assert abs(sum(pat) - 4) < 1e-6
