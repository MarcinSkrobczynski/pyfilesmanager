import pathlib

import click

from pyfilesmanager import __version__
from pyfilesmanager.files.finder import find_duplicate_files
from pyfilesmanager.utils.debugger import print_arguments


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


@main.command()
@click.pass_context
@click.argument("dir_path", nargs=1, type=click.Path(exists=True, path_type=pathlib.Path))
@click.option(
    "--output-dir",
    default=".",
    show_default=True,
    type=click.Path(file_okay=False, writable=True, path_type=pathlib.Path),
    help="Directory where debug files are written.",
)
def find_duplicates(ctx: click.Context, dir_path: pathlib.Path, output_dir: pathlib.Path):
    debug = ctx.obj["debug"]
    if debug:
        print_arguments(dir_path=dir_path, output_dir=output_dir)

    duplicate_files = find_duplicate_files(dir_path, debug=debug, output_dir=output_dir)

    if duplicate_files:
        click.echo(f"Found {len(duplicate_files)} duplicate files")
        for file_hash, paths in duplicate_files.items():
            click.echo(f"\nHash: {file_hash}")
            for path in paths:
                click.echo(f"- {path}")
    else:
        click.echo("No duplicate files found.")


if __name__ == "__main__":
    main()
