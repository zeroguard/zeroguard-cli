"""ZeroGuard platform availability/status check command."""
import click


@click.command()
@click.pass_context
def status(ctx):
    """Print ZeroGuard platform availability status."""
    raise NotImplementedError()
