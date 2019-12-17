"""."""
import click

from zgcli.config import DEFAULT_CONFIG
import zgcli.validators as validators


OPT_INCLUDE_RESOURCES_KWARGS = {
    'help': (
        'List of resources with their singular views to include in the output.'
    ),
    'metavar': 'RES',
    'multiple': True
}


@click.command()
@click.option('-i', '--include-resources', **OPT_INCLUDE_RESOURCES_KWARGS)
@click.argument('pattern')
@click.pass_context
def domain(ctx, **options):
    """Get intelligence about matching Internet domain names."""
    print(options)
