from jazzgen.data.fetch import sha256
from pathlib import Path
import tempfile


def test_sha256(tmp_path: Path):
    data = b"hello"
    file = tmp_path / "x.txt"
    file.write_bytes(data)
    assert sha256(file) == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
