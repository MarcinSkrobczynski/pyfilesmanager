import pathlib

from pyfilesmanager.files.scanner import collect_valid_files


def test_collect_valid_files_empty_dir(tmp_path: pathlib.Path) -> None:
    result = collect_valid_files(tmp_path)
    assert result == []


def test_collect_valid_files_returns_files(tmp_path: pathlib.Path) -> None:
    (tmp_path / "a.txt").write_bytes(b"hello")
    (tmp_path / "b.txt").write_bytes(b"world")

    result = collect_valid_files(tmp_path)

    assert len(result) == 2
    assert set(result) == {tmp_path / "a.txt", tmp_path / "b.txt"}


def test_collect_valid_files_skips_empty_files(tmp_path: pathlib.Path) -> None:
    non_empty = tmp_path / "data.txt"
    non_empty.write_bytes(b"content")
    (tmp_path / "empty.txt").write_bytes(b"")

    result = collect_valid_files(tmp_path)

    assert result == [non_empty]


def test_collect_valid_files_skips_symlinks(tmp_path: pathlib.Path) -> None:
    real_file = tmp_path / "real.txt"
    real_file.write_bytes(b"data")
    link = tmp_path / "link.txt"
    link.symlink_to(real_file)

    result = collect_valid_files(tmp_path)

    assert result == [real_file]


def test_collect_valid_files_recursive(tmp_path: pathlib.Path) -> None:
    root_file = tmp_path / "root.txt"
    root_file.write_bytes(b"root")
    subdir = tmp_path / "sub"
    subdir.mkdir()
    sub_file = subdir / "nested.txt"
    sub_file.write_bytes(b"nested")

    result = collect_valid_files(tmp_path)

    assert set(result) == {root_file, sub_file}
