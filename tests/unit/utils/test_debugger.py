import click
from click.testing import CliRunner

from pyfilesmanager.utils.debugger import print_arguments


def _capture(runner: CliRunner, **kwargs) -> str:
    """Invoke print_arguments inside a Click runner to capture output."""

    @click.command()
    def _cmd():
        print_arguments(**kwargs)

    result = runner.invoke(_cmd)
    return result.output


def test_print_arguments_no_args():
    runner = CliRunner()
    output = _capture(runner)
    assert "Arguments:" in output


def test_print_arguments_single_arg(tmp_path):
    runner = CliRunner()
    output = _capture(runner, path=str(tmp_path / "foo"))
    assert f"path = {tmp_path / 'foo'}" in output


def test_print_arguments_multiple_args(tmp_path):
    runner = CliRunner()
    output = _capture(runner, path=str(tmp_path / "foo"), debug=True)
    assert f"path = {tmp_path / 'foo'}" in output
    assert "debug = True" in output
