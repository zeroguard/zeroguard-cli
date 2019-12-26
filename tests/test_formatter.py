"""Test zgcli.formatter module."""
# pylint: disable=E0401,E0611
from zgcli.formatter import Formatter
from zgcli.formatter import DEFAULT_FORMATTER as fmt


def test_dummy_output():
    """Dummy test to verify formatter module does not crush.

    NOTE: This test function only ensures the formatter module does not crash.
    Actual output is verified manually, using human eyes -_-.
    """
    test_output_data = {'value': "Some value"}
    test_jinja_template = """
    Example template:
    {% for item in range(2) %}
        {t.blue} {{item}} {{value.center(40,'#')}}
    {% endfor %}
    """

    # Test colored output to STDOUT
    fmt.stdout = True
    fmt.colored = True
    fmt.force_colored = True

    fmt.info('msg info {t.blue}{t.underline} blue underline{t.normal}')
    fmt.warn('msg warn {t.red}{t.bold}red bold{t.normal}')
    fmt.err(test_jinja_template, test_output_data)
    fmt.ok('msg ok')
    fmt.data('msg data')

    # Test not colored output to STDERR
    fmt.stdout = False
    fmt.colored = False
    fmt.force_colored = False
    Formatter.VERBOSITY_LEVEL = Formatter.VERBOSITY_LEVELS.ERR

    fmt.info('msg info {t.blue}{t.underline} blue underline{t.normal}')
    fmt.warn('msg warn {t.red}{t.bold}red bold{t.normal}')
    fmt.err(test_jinja_template, test_output_data)
    fmt.ok('msg ok')
    fmt.data('msg data')

    # Test item list behaviour
    with fmt.itemlist(2):
        fmt.data("inside itemlist")
        fmt.ok("inside itemlist")
    fmt.data("outside itemlist")

    # Test numbered list behaviour
    with fmt.numlist(2):
        fmt.data("inside numlist")
        fmt.ok("inside numlist")
    fmt.fmt_print("outside numlist")
