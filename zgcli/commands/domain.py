"""."""
import click
import sys

from zgcli.config import DEFAULT_CONFIG


@click.command()
@click.argument('pattern')
@click.pass_context
def domain(ctx):
    """Get intelligence about matching Internet domain names."""
    raise NotImplementedError()
