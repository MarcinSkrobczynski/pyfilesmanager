import pathlib
from unittest.mock import patch

from click.testing import CliRunner

from pyfilesmanager import __version__
from pyfilesmanager.cli import main

# ---------------------------------------------------------------------------
# main (group)
# ---------------------------------------------------------------------------


def test_main_debug_off(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["--no-debug", "version", str(tmp_path)])
    assert "Debug mode is on" not in result.output


def test_main_debug_on(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["--debug", "version", str(tmp_path)])
    assert "Debug mode is on" in result.output


# ---------------------------------------------------------------------------
# version
# ---------------------------------------------------------------------------


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.output


# ---------------------------------------------------------------------------
# find_duplicates
# ---------------------------------------------------------------------------


def test_find_duplicates_no_duplicates(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"hello")
    (tmp_path / "b.txt").write_bytes(b"world")
    runner = CliRunner()
    result = runner.invoke(main, ["find-duplicates", str(tmp_path)])
    assert result.exit_code == 0
    assert "No duplicate files found." in result.output


def test_find_duplicates_with_duplicates(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"same")
    (tmp_path / "b.txt").write_bytes(b"same")
    runner = CliRunner()
    result = runner.invoke(main, ["find-duplicates", str(tmp_path)])
    assert result.exit_code == 0
    assert "Found 1 duplicate files" in result.output
    assert "Hash:" in result.output


def test_find_duplicates_invalid_dir():
    runner = CliRunner()
    result = runner.invoke(main, ["find-duplicates", "/nonexistent/path"])
    assert result.exit_code != 0


def test_find_duplicates_debug_prints_arguments(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["--debug", "find-duplicates", str(tmp_path)])
    assert "dir_path" in result.output
    assert "output_dir" in result.output


def test_find_duplicates_custom_output_dir(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    out = tmp_path / "out"
    out.mkdir()
    (src / "a.txt").write_bytes(b"same")
    (src / "b.txt").write_bytes(b"same")

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--debug", "find-duplicates", str(src), "--output-dir", str(out)],
    )
    assert result.exit_code == 0
    assert (out / "duplicates.txt").exists()


def test_find_duplicates_calls_find_duplicate_files(tmp_path):
    with patch("pyfilesmanager.cli.find_duplicate_files", return_value={}) as mock_fn:
        runner = CliRunner()
        runner.invoke(main, ["find-duplicates", str(tmp_path)])
        mock_fn.assert_called_once_with(
            pathlib.Path(str(tmp_path)),
            debug=False,
            output_dir=pathlib.Path("."),
        )
