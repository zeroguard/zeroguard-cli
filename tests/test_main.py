"""Test root CLI command which is implemented in zgcli.main module."""
# pylint: disable=E0611
from zgcli.main import create_cli


def test_create_cli():
    """Dummy test to make sure create_cli() function does not crash."""
    create_cli()


def test_cli(cli_runner):
    """Test root CLI command initialization and arguments validation."""
    cli_runner(['-h'])
    # TODO: Implement
