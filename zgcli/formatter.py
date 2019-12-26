"""Output formatter module."""
from contextlib import contextmanager
from functools import wraps
import re
import sys

import blessings
from jinja2 import Template
from box import Box
import colorama  # FIXME: Initialize colorama


def set_verbosity_level(verbosity_level):
    """Register verbosity level in function passed to the decorator.

    :param verbosity_level Specifies verbosity level of output, values should
                            be defined in `Formatter.VERBOSITY_LEVELS`
                            :class:`Box` in key-value format
    :type verbosity_level: int, required
    """
    def decorator_set_verbosity_level(func):

        @wraps(func)
        def wrapped_func(*args, **kwargs):

            # Register function to verbosity_level
            if not wrapped_func.registered:
                for level_value in Formatter.VERBOSITY_LEVELS.values():
                    if level_value <= verbosity_level:
                        level_dict = Formatter.VERBOSITY_LEVEL_DICT.get(
                            level_value, set())

                        level_dict.add(func.__name__)
                        Formatter.VERBOSITY_LEVEL_DICT[
                            level_value] = level_dict

            # Mark function as registered
            wrapped_func.registered = True

            # Filter function according verbosity level
            if func.__name__ in Formatter.VERBOSITY_LEVEL_DICT.get(
                    Formatter.VERBOSITY_LEVEL, set()):
                return func(*args, **kwargs)
            return None

        # Initialize function attribute
        wrapped_func.registered = False
        return wrapped_func

    return decorator_set_verbosity_level


class Formatter():
    """Format output from strings/templates.

    :param stdout:        Set output to SDTOUT/SDTERR, defaults to
                          `Formatter.DEFAULT_STDOUT`.
    :param colored:       Set coloring formatting to the output, defaults to
                          `Formatter.DEFAULT_COLORED`.
    :param force_colored: Set force styling when it's being piped to
                          another command/file, defaults to
                          `Formatter.DEFAULT_FORCE_COLORED`.

    :type stdout: bool, optional.
    :type colored: bool, optional.
    :type force_colored: bool, optional.
    """

    DEFAULT_MSG_ERR_PREF = '---(X) ERR: '
    DEFAULT_MSG_ERR_COLOR = '{t.red}'

    DEFAULT_MSG_INFO_PREF = '---(i) INFO: '
    DEFAULT_MSG_INFO_COLOR = '{t.white}'

    DEFAULT_MSG_OK_PREF = '---(+) OK: '
    DEFAULT_MSG_OK_COLOR = '{t.green}'

    DEFAULT_MSG_WARN_PREF = '---(!) WARN: '
    DEFAULT_MSG_WARN_COLOR = '{t.yellow}'

    DEFAULT_ITEMLIST_PREF = '* '
    DEFAULT_NUMLIST_PREF = '%i. '

    DEFAULT_INDENT = 0
    DEFAULT_INDENT_STEP = 2

    # If set to False, will send messages to STDERR
    DEFAULT_STDOUT = False
    DEFAULT_COLORED = True
    DEFAULT_FORCE_COLORED = False

    VERBOSITY_LEVELS = Box({
        'INFO':   0,
        'OK':     1,
        'WARN':   2,
        'ERR':    3
    })

    DEFAULT_VERBOSITY_LEVEL = VERBOSITY_LEVELS.INFO
    VERBOSITY_LEVEL = DEFAULT_VERBOSITY_LEVEL
    VERBOSITY_LEVEL_DICT = dict({DEFAULT_VERBOSITY_LEVEL: set()})

    # Regex for detecting templates formatting
    STRING_FORMATTING_REGEX = r'{[\w:._^<>]+}'
    # Regex for detecting Jinja2 templates
    JINJA_TEMPLATE_REGEX = r'{{.+}}|{%.+%}|{#.+#}|#.+##'

    def __init__(
            self,
            stdout=DEFAULT_STDOUT,
            colored=DEFAULT_COLORED,
            force_colored=DEFAULT_FORCE_COLORED
    ):
        """Construct Formatter instance."""
        self._stdout = stdout
        self._colored = colored
        self._force_colored = force_colored
        self._terminal = blessings.Terminal(
            force_styling=Formatter.DEFAULT_FORCE_COLORED)

    @staticmethod
    def create_from_defaults():
        """Create :class:`Formatter` instance from defaults.

        :return: :class:`Formatter` instance
        rtype:   :class:`Formatter`.
        """
        return Formatter()

    @property
    def stdout(self):
        """Get stdout property.

        :return: stdout property.
        :rtype:  bool.
        """
        return self._stdout

    @stdout.setter
    def stdout(self, value):
        """Set stdout property.

        :param value: stdout flag.
        :type value:  bool.
        """
        self._stdout = value

    @property
    def colored(self):
        """Get colored property.

        :return: colored property.
        :rtype:  bool.
        """
        return self._colored

    @colored.setter
    def colored(self, value):
        """Set colored property.

        :param value: colored flag.
        :type value:  bool.
        """
        self._colored = value

    @property
    def force_colored(self):
        """Get force_colored property.

        :return: force_colored property.
        :rtype: bool.
        """
        return self._force_colored

    @force_colored.setter
    def force_colored(self, value):
        """Set force_colored property.

        :param value: force_colored flag.
        :type value:  bool.
        """
        self._force_colored = value
        self._terminal = blessings.Terminal(force_styling=value)

    @set_verbosity_level(VERBOSITY_LEVELS.INFO)
    def info(self, template, data=None):
        """Print output of infos() method.

        Print output to the terminal when verbosity level is set to
        `Formatter.VERBOSITY_LEVEL = Formatter.VERBOSITY_LEVELS.INFO` or
        preceding level in the verbosity stack.
        """
        self.fmt_print(self.infos(template, data))

    def infos(self, template, data=None):
        """Build 'info' string using fmt_to_string() method.

        Additionally format output by coloring output into
        `Formatter.DEFAULT_MSG_INFO_COLOR` and add prefix at the beginning of
        message `Formatter.DEFAULT_MSG_INFO_PREF`.

        """
        info_template = '{}{}{}'.format(
            Formatter.DEFAULT_MSG_INFO_COLOR,
            Formatter.DEFAULT_MSG_INFO_PREF,
            template
        )
        info_template += '{t.normal}'

        return self.fmt_to_string(info_template, data)

    @set_verbosity_level(VERBOSITY_LEVELS.WARN)
    def warn(self, template, data=None):
        """Print output of warns() method.

        Print output to the terminal when verbosity level is set to
        `Formatter.VERBOSITY_LEVEL = Formatter.VERBOSITY_LEVELS.WARN` or
        preceding level in the verbosity stack.
        """
        self.fmt_print(self.warns(template, data))

    def warns(self, template, data=None):
        """Build 'warning' string using fmt_to_string() method.

        Additionally format output by coloring output into
        `Formatter.DEFAULT_MSG_WARN_COLOR` and add prefix at the beginning of
        message `Formatter.DEFAULT_MSG_WARN_PREF`.
        """
        warn_template = '{}{}{}'.format(
            Formatter.DEFAULT_MSG_WARN_COLOR,
            Formatter.DEFAULT_MSG_WARN_PREF,
            template
        )
        warn_template += '{t.normal}'

        return self.fmt_to_string(warn_template, data)

    @set_verbosity_level(VERBOSITY_LEVELS.ERR)
    def err(self, template, data=None):
        """Print output of errs() method.

        Print output to the terminal when verbosity level is set to
        `Formatter.VERBOSITY_LEVEL = Formatter.VERBOSITY_LEVELS.ERR` or
        preceding level in the verbosity stack.
        """
        self.fmt_print(self.errs(template, data))

    def errs(self, template, data=None):
        """Build 'error' string using fmt_to_string() method.

        Additionally format output by coloring output into
        `Formatter.DEFAULT_MSG_ERR_COLOR` and add prefix at the beginning of
        message `Formatter.DEFAULT_MSG_ERR_PREF`.
        """
        err_template = '{}{}{}'.format(
            Formatter.DEFAULT_MSG_ERR_COLOR,
            Formatter.DEFAULT_MSG_ERR_PREF,
            template
        )
        err_template += '{t.normal}'

        return self.fmt_to_string(err_template, data)

    @set_verbosity_level(VERBOSITY_LEVELS.OK)
    def ok(self, template, data=None):  # pylint: disable=C0103
        """Print output of oks() method.

        Print output to the terminal when verbosity level is set to
        `Formatter.VERBOSITY_LEVEL = Formatter.VERBOSITY_LEVELS.OK` or
        preceding level in the verbosity stack.
        """
        self.fmt_print(self.oks(template, data))

    def oks(self, template, data=None):
        """Build 'ok' string using fmt_to_string() method.

        Additionally format output by coloring output into
        `Formatter.DEFAULT_MSG_OK_COLOR` and add prefix at the beginning of
        message `Formatter.DEFAULT_MSG_OK_PREF`.
        """
        ok_template = '{}{}{}'.format(
            Formatter.DEFAULT_MSG_OK_COLOR,
            Formatter.DEFAULT_MSG_OK_PREF,
            template
        )
        ok_template += '{t.normal}'

        return self.fmt_to_string(ok_template, data)

    def data(self, template, data=None):
        """Print output of datas() method."""
        self.fmt_print(self.datas(template, data))

    def datas(self, template, data=None):
        """Build 'data' string using fmt_to_string() method."""
        return self.fmt_to_string(template, data)

    @contextmanager
    def itemlist(self, indent=DEFAULT_INDENT):
        """Activate item list context manager.

        Modify behavior of fmt_to_string() method by adding extra prefix
        `Formatter.DEFAULT_ITEMLIST_PREF` and override indent in fmt_print()
        method.

        :param indent: Specify output indent, defaults to
                       `Formatter.DEFAULT_INDENT`.
        :type indent:  int, optional.
        """
        fmt_to_string = self.fmt_to_string
        fmt_print = self.fmt_print

        @wraps(fmt_to_string)
        def wrapped_fmt_to_string(*args, **kwargs):
            return fmt_to_string(
                *args, prefix=Formatter.DEFAULT_ITEMLIST_PREF, **kwargs)

        @wraps(fmt_print)
        def wrapped_fmt_print(*args, **kwargs):
            return fmt_print(*args, indent=indent, **kwargs)

        setattr(self, 'fmt_to_string', wrapped_fmt_to_string)
        setattr(self, 'fmt_print', wrapped_fmt_print)

        yield

        setattr(self, 'fmt_to_string', fmt_to_string)
        setattr(self, 'fmt_print', fmt_print)

    @contextmanager
    def numlist(self, indent=DEFAULT_INDENT):
        """Activate number list context manager.

        Modifies behavior of fmt_to_string() method by adding extra template of
        the prefix `Formatter.DEFAULT_NUMLIST_PREF` which is filled with
        a number of recent method's calls count and overrides indent
        in fmt_print() method.

        :param indent: Specify output indent, defaults to
                       `Formatter.DEFAULT_INDENT`.
        :type indent:  int, optional.
        """
        fmt_to_string = self.fmt_to_string
        fmt_print = self.fmt_print

        @wraps(fmt_to_string)
        def wrapped_fmt_to_string(*args, **kwargs):
            wrapped_fmt_to_string.num_calls += 1
            prefix = Formatter.DEFAULT_NUMLIST_PREF % \
                wrapped_fmt_to_string.num_calls

            return fmt_to_string(*args, prefix=prefix, **kwargs)

        wrapped_fmt_to_string.num_calls = 0

        @wraps(fmt_print)
        def wrapped_fmt_print(*args, **kwargs):
            return fmt_print(*args, indent=indent, **kwargs)

        setattr(self, 'fmt_to_string', wrapped_fmt_to_string)
        setattr(self, 'fmt_print', wrapped_fmt_print)

        yield

        setattr(self, 'fmt_to_string', fmt_to_string)
        setattr(self, 'fmt_print', fmt_print)

    def fmt_print(self, *args, indent=DEFAULT_INDENT, **kwargs):
        """Format input data and print it out.

        Directs output to `sys.stderr` or `sys.stderr` according to the value
        of `self.stdout` property

        :param indent: Specify output indent, defaults to
                       `Formatter.DEFAULT_INDENT`.
        :type indent:  int, optional.
        """
        output = sys.stderr
        if self.stdout:
            output = sys.stdout

        if indent > 0:
            indent = ' ' * indent * Formatter.DEFAULT_INDENT_STEP
            print(indent, *args, file=output, **kwargs)
            return

        print(*args, file=output, **kwargs)

    def fmt_to_string(self, template, data=None, prefix=None):
        """Build strind output from template, insert data and formatting in it.

        Formatting is regulated by `self.colored` property.

        Template can be:
            1. Literal string to output without any extra steps
            2. Jinja2 + format()-able template to colorize and then pass
            through Jinja2 and then output (data contains actual
            values to use).

        :param template: Tem
        :param data:     Data contains actual values to fill Jinja2 template,
                         defaults to None.
        :param prefix:   Optional prefix at the beginning of message.

        :type template: string, :class:`Jinja2.Template`, required.
        :type data:     dict, optional.
        :type prefix:   string, optional.

        :return: Formatted string.
        :rtype: string.
        """
        if re.search(Formatter.JINJA_TEMPLATE_REGEX, template):
            template = Template(template).render(data)

        if self.colored:
            string = template.format(t=self._terminal)
        else:
            string = re.sub(Formatter.STRING_FORMATTING_REGEX, '', template)

        if prefix:
            string = '{}{}'.format(prefix, string)

        return string


# Create a singletone default Formatter instance
DEFAULT_FORMATTER = Formatter.create_from_defaults()
