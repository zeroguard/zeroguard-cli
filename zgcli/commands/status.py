"""."""
import click


@click.command()
@click.pass_context
def status(ctx):
    """."""
    print('Dummy status command')
