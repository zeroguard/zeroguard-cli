"""Test zgcli.formatter module."""
from zgcli.formatter import Formatter
from zgcli.formatter import DEFAULT_FORMATTER as fmt


def test_dummy_output():
    """Dummy test to verify formatter module does not crush."""
    TEST_JINJA_TEMPLATE = """
    Example template:
    {% for item in range(2) %}
        {t.blue} {{item}} {{value.center(40,'#')}}
    {% endfor %}
    """

    TEST_OUTPUT_DATA = {'value': "Some value"}

    fmt.stdout = True
    fmt.colored = True
    fmt.force_colored = True

    fmt.info('msg info {t.blue}{t.underline} blue underline{t.normal}')
    fmt.warn('msg warn {t.red}{t.bold}red bold{t.normal}')
    fmt.err(TEST_JINJA_TEMPLATE, TEST_OUTPUT_DATA)
    fmt.ok('msg ok')
    fmt.data('msg data')

    fmt.stdout = False
    fmt.colored = False
    fmt.force_colored = False
    Formatter.VERBOSITY_LEVEL = Formatter.VERBOSITY_LEVELS.ERR

    fmt.info('msg info {t.blue}{t.underline} blue underline{t.normal}')
    fmt.warn('msg warn {t.red}{t.bold}red bold{t.normal}')
    fmt.err(TEST_JINJA_TEMPLATE, TEST_OUTPUT_DATA)
    fmt.ok('msg ok')
    fmt.data('msg data')

    with fmt.itemlist(2):
        fmt.data("inside itemlist")
        fmt.ok("inside itemlist")
    fmt.data("outside itemlist")

    with fmt.numlist(2):
        fmt.data("inside numlist")
        fmt.ok("inside numlist")
    fmt.fmt_print("outside numlist")
