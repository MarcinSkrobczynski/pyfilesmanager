import click


def print_arguments(**kwargs):
    click.secho("Arguments:", fg="cyan")
    for key, value in kwargs.items():
        click.secho(f"- {key} = {value}", fg="cyan")

    click.echo("\n")
