import pathlib

import click

from pyfilesmanager import __version__


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def main(ctx: click.Context, debug: bool):
    """Files manager utilities."""
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    if debug:
        click.secho("Debug mode is on", fg="yellow")


@main.command()
def version():
    """Show the version of pyfilesmanager."""
    click.echo(__version__)


if __name__ == "__main__":
    main()
