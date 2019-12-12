"""Test zgcli.validators module."""
# pylint: disable=E0401,E0611
import zgcli.validators as validators


def test_check_valid_netloc():
    """Test zgcli.validators.check_valid_netloc function."""
    good_cases = [
        'foo.bar.baz',
        'bar.baz',
        '42.33.foo',
        '4.xxx'
        '42.42.42.xxd',
        '42.42.42.42',
        'one-two.foo'
    ]

    for case in good_cases:
        assert validators.check_valid_netloc(case)

    bad_cases = [
        'foo.t4',
        'bruh',
        '777',
        '::42',
        '333:33::fff',
        '-bruh.dev-',

        # FIXME: This should be invalid
        # '355.0.0.1',
        # '-bruh.com',
        # 'bruh-.net',
    ]

    for case in bad_cases:
        assert not validators.check_valid_netloc(case)
