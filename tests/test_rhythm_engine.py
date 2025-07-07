from jazzgen.rhythm_engine import quantise

def test_quantise_simple():
    times = quantise([0.5, 0.5, 1.0])
    assert len(times) == 3
    assert times[0][0] == 0
    assert times[-1][1] == 2.0
