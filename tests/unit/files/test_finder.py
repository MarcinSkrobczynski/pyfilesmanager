from unittest.mock import patch

import click
from click.testing import CliRunner

from pyfilesmanager.files.finder import _hash_candidates, _write_debug_files, find_duplicate_files

# ---------------------------------------------------------------------------
# _hash_candidates
# ---------------------------------------------------------------------------


def test_hash_candidates_groups_duplicates(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_bytes(b"same content")
    b.write_bytes(b"same content")

    result, failures = _hash_candidates([a, b], "test", bytes_limit=None)

    assert failures == []
    assert len(result) == 1
    group = next(iter(result.values()))
    assert set(group) == {a, b}


def test_hash_candidates_empty():
    result, failures = _hash_candidates([], "test")
    assert result == {}
    assert failures == []


def test_hash_candidates_reports_failure(tmp_path):
    p = tmp_path / "file.txt"
    p.write_bytes(b"data")

    with patch("pyfilesmanager.files.finder.compute_hash", side_effect=OSError("read error")):
        result, failures = _hash_candidates([p], "test")

    assert result == {}
    assert len(failures) == 1
    assert failures[0][0] == p


# ---------------------------------------------------------------------------
# _write_debug_files
# ---------------------------------------------------------------------------


def test_write_debug_files(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_bytes(b"x")
    b.write_bytes(b"x")

    fake_hash = "abc123"
    _write_debug_files({fake_hash: [a, b]}, tmp_path)

    out = tmp_path / "duplicates.txt"
    assert out.exists()
    content = out.read_text()
    assert fake_hash in content


# ---------------------------------------------------------------------------
# find_duplicate_files
# ---------------------------------------------------------------------------


def test_find_duplicate_files_empty_dir(tmp_path):
    assert find_duplicate_files(tmp_path) == {}


def test_find_duplicate_files_no_size_candidates(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"hello")
    (tmp_path / "b.txt").write_bytes(b"world!")
    assert find_duplicate_files(tmp_path) == {}


def test_find_duplicate_files_no_duplicates(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"hello")
    (tmp_path / "b.txt").write_bytes(b"world")  # same size, different content
    result = find_duplicate_files(tmp_path)
    assert result == {}


def test_find_duplicate_files_with_duplicates(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"same content")
    (tmp_path / "b.txt").write_bytes(b"same content")
    result = find_duplicate_files(tmp_path)
    assert len(result) == 1
    group = next(iter(result.values()))
    assert len(group) == 2


def test_find_duplicate_files_debug_prints_stages(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"same")
    (tmp_path / "b.txt").write_bytes(b"same")

    @click.command()
    def _cmd():
        find_duplicate_files(tmp_path, debug=True, output_dir=tmp_path)

    result = CliRunner().invoke(_cmd)
    assert "Stage 1" in result.output
    assert "Stage 2" in result.output


def test_find_duplicate_files_debug_writes_files(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"same")
    (tmp_path / "b.txt").write_bytes(b"same")

    @click.command()
    def _cmd():
        find_duplicate_files(tmp_path, debug=True, output_dir=tmp_path)

    CliRunner().invoke(_cmd)
    assert (tmp_path / "duplicates.txt").exists()


def test_find_duplicate_files_reports_hash_failure(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"data")
    (tmp_path / "b.txt").write_bytes(b"data")
    bad = tmp_path / "a.txt"

    @click.command()
    def _cmd():
        with patch("pyfilesmanager.files.finder._hash_candidates") as mock:
            mock.return_value = ({}, [(bad, OSError("permission denied"))])
            find_duplicate_files(tmp_path)

    result = CliRunner().invoke(_cmd)
    assert "Failed to hash" in result.output
