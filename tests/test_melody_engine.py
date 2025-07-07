from jazzgen.melody_engine import compose


def test_compose_simple():
    chords = [("C", "7"), ("F", "7")]
    events = compose(chords, seed=123)
    assert len(events) > 0
    assert all(len(ev) == 3 for ev in events)
