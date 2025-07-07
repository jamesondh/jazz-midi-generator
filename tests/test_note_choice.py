from jazzgen.note_choice import pick_pitch


def test_pick_pitch():
    pitch = pick_pitch(("C", "7"), None)
    assert isinstance(pitch, int)
    assert 60 <= pitch <= 84
