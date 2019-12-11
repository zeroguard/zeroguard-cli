"""ZeroGuard CLI entrypoint and root commmand."""
import sys

import click

from zgcli import __description__, __version__, DEFAULT_CONFIG
from zgcli.commands import ENABLED_COMMANDS


CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help'],
    'max_content_width': DEFAULT_CONFIG.display.max_content_width
}


OPT_API_TOKEN_KWARGS = {
    'help': 'API token to use for authentication.',
    'metavar': 'TOKEN'
}


OPT_LOG_KWARGS = {
    'help': 'Enable application logging.',
    'default': False,
    'is_flag': True
}


OPT_LOG_FORMAT_KWARGS = {
    'help': 'Logging format to use if logging is enabled.',
    'default': DEFAULT_CONFIG.logging.log_format,
    'metavar': 'FORMAT',
    'show_default': True,
    'type': click.Choice(DEFAULT_CONFIG.logging.acceptable_log_formats)
}


OPT_LOG_LEVEL_KWARGS = {
    'help': 'Logging level to set if logging is enabled.',
    'default': DEFAULT_CONFIG.logging.log_level,
    'metavar': 'LEVEL',
    'show_default': True,
    'type': click.Choice(DEFAULT_CONFIG.logging.acceptable_log_levels)
}


OPT_LOG_STDOUT_KWARGS = {
    'help': 'Output log messages to STDOUT if logging is enabled.',
    'default': False,
    'is_flag': True
}


OPT_OUTPUT_FORMAT_KWARGS = {
    'help': 'Data output format.',
    'default': DEFAULT_CONFIG.display.output_format,
    'metavar': 'FORMAT',
    'show_default': True,
    'type': click.Choice(DEFAULT_CONFIG.display.acceptable_output_formats)
}


OPT_QUIET_KWARGS = {
    'help': 'Suppress application informational messages.',
    'default': False,
    'is_flag': True
}


OPT_VERSION_KWARGS = {
    'help': 'Show application version and exit.',
    'default': False,
    'is_flag': True
}


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option('-t', '--api-token', **OPT_API_TOKEN_KWARGS)
@click.option('-L', '--log', **OPT_LOG_KWARGS)
@click.option('-F', '--log-format', **OPT_LOG_FORMAT_KWARGS)
@click.option('-l', '--log-level', **OPT_LOG_LEVEL_KWARGS)
@click.option('-S', '--log-stdout', **OPT_LOG_STDOUT_KWARGS)
@click.option('-f', '--output-format', **OPT_OUTPUT_FORMAT_KWARGS)
@click.option('-q', '--quiet', **OPT_QUIET_KWARGS)
@click.option('-v', '-V', '--version', **OPT_VERSION_KWARGS)
@click.pass_context
def cli(ctx, **options):
    """."""
    # Print CLI version if requested
    if options['version']:
        click.echo('%s version %s' % (__description__, __version__))
        sys.exit(0)

    # Print help if no subcommand was specified
    if ctx.invoked_subcommand is None:
        click.echo(cli.get_help(ctx))
        sys.exit(0)


def create_cli(nowrap=False):
    """Prepare CLI application object for usage.

    :param nowrap: Do not wrap CLI into a lambda function which passes context
                   objext. This parameters is mostly needed for testing.
    :type nowrap:  bool

    :return: CLI instance ready to be run
    :rtype:  func
    """
    for command in ENABLED_COMMANDS:
        cli.add_command(command)

    # pylint: disable=E1120,E1123
    return cli if nowrap else lambda: cli(obj={})


# Run ZeroGuard CLI application if called directly
if __name__ == '__main__':
    create_cli()()
