from jazzgen.data.build_chord_corpus import parse_symbol, parse_song


def test_parse_symbol():
    assert parse_symbol("G7alt") == ("G", "7alt")
    assert parse_symbol("Bbmaj7") == ("Bb", "maj7")


def test_parse_song():
    song = {
        "Title": "Dummy",
        "Key": "F",
        "Sections": [
            {"MainSegment": {"Chords": "F7|Bb7"}}
        ],
    }
    parsed = parse_song(song)
    assert parsed == [[("C", "7")], [("F", "7")]]
