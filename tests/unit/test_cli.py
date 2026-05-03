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
