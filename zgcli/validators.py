"""Data validation functions."""
import re

from click import BadParameter

# FIXME: This is far from being perfect. See tests/test_validators.py for
# commented out bad cases that pass. The question though, should it be perfect?
NETLOC_RE = re.compile((
    r'^([a-z0-9\-\.]*)\.(([a-z]{2,4})|([0-9]{1,3}\.([0-9]{1,3})'
    r'\.([0-9]{1,3})))(:[0-9]{2,5})?$'
), flags=re.IGNORECASE)


def check_valid_netloc_click(_, __, value):
    """Click compatible wrapper around network location validator."""
    valid_netlock = check_valid_netloc(value)

    if not valid_netlock:
        raise BadParameter('API endpoint specified is not valid.')


def check_valid_netloc(string):
    """Check whether given string represents a valid network location.

    Please note that this validator does not guarantee that IPv4 address is
    valid (i.e. 355.0.0.1 will return True). This will still ensure IPv4 has a
    correct structure, just without 0-255 integer values for each octet.

    :param string:        String to validate
    :type string:        str

    :return: Validation result
    :rtype:  bool
    """
    return bool(NETLOC_RE.match(string))
