"""PyTest fixtures."""
from click.testing import CliRunner
import pytest

# pylint: disable=C0411,E0611
from zgcli.main import create_cli


@pytest.fixture(scope='session')
def cli_runner():
    """Create a fresh instance of CLI test runner."""
    runner = CliRunner()
    cli = create_cli(nowrap=True)

    return lambda *args, **kwargs: runner.invoke(cli, *args, **kwargs, obj={})
