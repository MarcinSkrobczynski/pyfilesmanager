import hashlib

from pyfilesmanager.files.hasher import compute_hash


def test_compute_hash_full(tmp_path):
    f = tmp_path / "file.bin"
    f.write_bytes(b"hello world")
    result = compute_hash(f)
    assert len(result) == 64
    assert all(c in "0123456789abcdef" for c in result)


def test_compute_hash_same_content_same_hash(tmp_path):
    content = b"same content"
    f1 = tmp_path / "a.bin"
    f2 = tmp_path / "b.bin"
    f1.write_bytes(content)
    f2.write_bytes(content)
    assert compute_hash(f1) == compute_hash(f2)


def test_compute_hash_different_content_different_hash(tmp_path):
    f1 = tmp_path / "a.bin"
    f2 = tmp_path / "b.bin"
    f1.write_bytes(b"content one")
    f2.write_bytes(b"content two")
    assert compute_hash(f1) != compute_hash(f2)


def test_compute_hash_partial(tmp_path):
    content = b"abcdefghij"  # 10 bytes
    f = tmp_path / "file.bin"
    f.write_bytes(content)
    partial = compute_hash(f, bytes_limit=4)
    full = compute_hash(f)
    expected_partial = hashlib.sha256(content[:4]).hexdigest()
    assert partial == expected_partial
    assert partial != full


def test_compute_hash_partial_equals_full_when_file_smaller(tmp_path):
    content = b"abc"  # 3 bytes
    f = tmp_path / "file.bin"
    f.write_bytes(content)
    assert compute_hash(f, bytes_limit=10) == compute_hash(f)
