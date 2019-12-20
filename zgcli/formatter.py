"""Output formatter module."""
# from __future__ import print_function
from contextlib import contextmanager
from functools import wraps
from box import Box
import logging
import sys
import re
# TODO: These libraries should provide low level building blocks for this
# module. Feel free to add other dependencies if required but please make sure
# we avoid adding a lot of "convenience" libraries if that can be easily
# implemented with what we already have in place.
import blessings
import colorama
from jinja2 import Template

def set_verbosity_level(verbosity_level):
    """Registers verbosity level in function passed to the decorator
    :param verbosity_level: Specifies verbosity level of output, values should be
                            defined in `Formatter.VERBOSITY_LEVELS` :class:`Box`
                            in key-value format
    :type verbosity_level: int, required
    """
    def decorator_set_verbosity_level(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if not wrapped_func.registered:
                for level_label, level_value in Formatter.VERBOSITY_LEVELS.items():
                    if level_value <= verbosity_level:
                        if Formatter.VERBOSITY_LEVEL_DICT.get(level_value) is not None:
                            Formatter.VERBOSITY_LEVEL_DICT[level_value].add(func.__name__)
                        else:
                            Formatter.VERBOSITY_LEVEL_DICT[level_value] = set([func.__name__])
            wrapped_func.registered = True
            if (Formatter.VERBOSITY_LEVEL_DICT.get(Formatter.VERBOSITY_LEVEL) and
                func.__name__ in Formatter.VERBOSITY_LEVEL_DICT[Formatter.VERBOSITY_LEVEL]):
                return func(*args, **kwargs)
        wrapped_func.registered = False
        return wrapped_func
    return decorator_set_verbosity_level

# Regex for detecting templates formatting
STRING_FORMATTING_REGEX = '{[\w:._^<>]+}'
# Regex for detecting Jinja2 templates
JINJA_TEMPLATE_REGEX = '{{.+}}|{%.+%}|{#.+#}|#.+##'


# NOTE: Do we want to inherit from logger? In a perfect world we'd want to,
# because that would allow us to get levels OOTB and easily conditionally
# disabled some messages.
#
# Again, this is a module for formatting CLI application output, not outputting
# logs. We will still have an ability to enable logging from CLI, but that is
# mostly for debugging how SDK and CLI work together. Logging and output
# produced by formatter should be completely independent.
class Formatter():
    """."""

    # Features:
    # 1. Automatically disable color if output is redirected (IIRC this is
    #    already handled by blessings library)
    #
    # 2. Colors should work on Linux, MacOS and Windows
    #
    # 3. Support for item lists and numbered lists using Python context
    #    managers. Would be nice to also provide a declarative interface (i.e.
    #    fmt.list_start() and fmt.list_end() or similar).
    #
    # 4. Support for 4 types of messages: INFO, WARNING, ERROR, OK. These are
    #    not logging levels but rather differently styled message types. ERROR
    #    ones will be red by default, WARNING ones - orange etc.
    #
    # 5. Support for custom message prefixes for each message type. See
    #    DEFAULT_MSG_* constants below, though we want to allow to override
    #    that in constructor (or even on the fly).
    #
    # 6. Support for indented messages (both context manager and declarative).
    #    This is similar to lists so might be a part of list functionality. See
    #    method signatures below.
    #
    # 7. Support for coloring (using blessings t.<style> and str.format()) and
    #    templating (using Jinja2). It should be possible to pass either inline
    #    template to fill out or a name of template file to load and fill out.
    #    See corresponding methods for details or ping dd directly.
    #
    # 8. Support for formatting and outputting tables. Similar to how psql
    #    handles it. Very optional, do not think about it too much right now,
    #    unless we can wrap a decent enough Python library that does all the
    #    heavy lifting for us.
    #
    # 9. Support for progress bars. Something very similar to:
    #    http://click.palletsprojects.com/en/7.x/utils/#showing-progress-bars
    #
    # 10. Support for paging. Essentially like zg ... | less -R but OOTB. Click
    #     does it but we can't use it directly:
    #     http://click.palletsprojects.com/en/7.x/utils/#pager-support
    #
    # Notes:
    # * We do not want to use any functionality provided by Click library, even
    #   though it has both rudimentary coloring and progress bar support.
    #   Chances are, Click will be stripped out for V2 and we want to keep our
    #   code as loosely coupled with it as it is possible.
    #
    # * Do not worry about Windows support too much for now. Make sure that
    #   MacOS and Linux are supported. We will fix other OS-specific issues
    #   later on.
    #
    # * If method signatures provided do not make sense for any reason, feel
    #   free to modify them. We need a more or less stable API exposed so we
    #   can get on with our business logic without refactoring prints for ages.
    #
    # * As always, make it DRY and KISS. If you feel that a particular feature
    #   forces you to get too much hax in place - abandon it for now.
    #
    # * Try to use underlying logger object to print everything out so we get
    #   levels OOTB and can disable some INFO stuff while keeping ERR and
    #   WARNING messages. Again, this should be completely independent from
    #   application log messages.
    #
    # * Add some extra features if they are easy to implement and make sense
    # (i.e. allow to override some instance defaults passing a kwarg to a
    # specific method etc.)
    #
    # * TDD please

    DEFAULT_MSG_ERR_PREF = '---(X) ERR: '
    DEFAULT_MSG_ERR_COLOR = '{t.red}'  # Red

    DEFAULT_MSG_INFO_PREF = '---(i) INFO: '
    DEFAULT_MSG_INFO_COLOR = '{t.white}'  # White

    DEFAULT_MSG_OK_PREF = '---(+) OK: '
    DEFAULT_MSG_OK_COLOR = '{t.green}'  # Green

    DEFAULT_MSG_WARN_PREF = '---(!) WARN: '
    DEFAULT_MSG_WARN_COLOR = '{t.yellow}'  # Orange

    DEFAULT_ITEMLIST_PREF = '* '
    DEFAULT_NUMLIST_PREF = '%i. '

    # NOTE: Preffer tabs over spaces for formatting. This will make it easier
    # to cut and sed output of your CLI. See if you can make tab to look like 2
    # spaces on CLI.
    DEFAULT_INDENT = 0
    DEFAULT_INDENT_STEP = 2

    # NOTE: Allow to output all messages to STDOUT
    STDOUT = False  # STDERR

    # NOTE: Output in color by default, unless output is redirected
    DEFAULT_COLORED = True

    # NOTE: Allow to force color even if redirected
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

    TERMINAL = blessings.Terminal(force_styling=DEFAULT_FORCE_COLORED)


    def __init__(self, **kwargs):
        """."""


    @staticmethod
    def set_force_colored(force_colored=DEFAULT_FORCE_COLORED):
        """Toggle force output coloring/styling to another command or redirected to a file

        :param force_colored: Sets force styling when it's being piped to another
                              command/file, defaults to Formatter.DEFAULT_FORCE_COLORED
        :type force_colored: bool, optional
        """
        Formatter.TERMINAL = blessings.Terminal(force_styling=force_colored)


    @set_verbosity_level(VERBOSITY_LEVELS.INFO)
    def info(self, template, data=None):
        """Same as data() but:
        * Additionally formats output by coloring output into
        `Formatter.DEFAULT_MSG_INFO_COLOR` and adds prefix at the beginning of message
        `Formatter.DEFAULT_MSG_INFO_PREF`
        * Prints output to the terminal when verbosity level is set to
        `Formatter.VERBOSITY_LEVEL = Formatter.VERBOSITY_LEVELS.INFO` or preceding
        level in the verbosity stack
        """
        self.fmt_print(self.infos(template, data))


    def infos(self, template, data=None):
        """Same as info() but do not print out and return as string"""
        info_template = '{}{}{}'.format(
            Formatter.DEFAULT_MSG_INFO_COLOR,
            Formatter.DEFAULT_MSG_INFO_PREF,
            template)+'{t.normal}'
        return self.fmt_to_string(info_template, data)


    @set_verbosity_level(VERBOSITY_LEVELS.WARN)
    def warn(self, template, data=None):
        """Same as data() but:
        * Additionally formats output by coloring output into
        `Formatter.DEFAULT_MSG_WARN_COLOR` and adds prefix at the beginning of message
        `Formatter.DEFAULT_MSG_WARN_PREF`
        * Prints output to the terminal when verbosity level is set to
        `Formatter.VERBOSITY_LEVEL = Formatter.VERBOSITY_LEVELS.WARN` or preceding
        level in the verbosity stack
        """
        self.fmt_print(self.warns(template, data))


    def warns(self, template, data=None):
        """Same as warn() but do not print out and return as string"""
        warn_template = '{}{}{}'.format(
            Formatter.DEFAULT_MSG_WARN_COLOR,
            Formatter.DEFAULT_MSG_WARN_PREF,
            template)+'{t.normal}'
        return self.fmt_to_string(warn_template, data)


    @set_verbosity_level(VERBOSITY_LEVELS.ERR)
    def err(self, template, data=None):
        """Same as data() but:
        * Additionally formats output by coloring output into
        `Formatter.DEFAULT_MSG_ERR_COLOR` and adds prefix at the beginning of message
        `Formatter.DEFAULT_MSG_ERR_PREF`
        * Prints output to the terminal when verbosity level is set to
        `Formatter.VERBOSITY_LEVEL = Formatter.VERBOSITY_LEVELS.ERR` or preceding
        level in the verbosity stack
        """
        self.fmt_print(self.errs(template, data))


    def errs(self, template, data=None):
        """Same as err() but do not print out and return as string"""
        err_template = '{}{}{}'.format(
            Formatter.DEFAULT_MSG_ERR_COLOR,
            Formatter.DEFAULT_MSG_ERR_PREF,
            template)+'{t.normal}'
        return self.fmt_to_string(err_template, data)


    @set_verbosity_level(VERBOSITY_LEVELS.OK)
    def ok(self, template, data=None):
        """Same as data() but:
        * Additionally formats output by coloring output into
        `Formatter.DEFAULT_MSG_OK_COLOR` and adds prefix at the beginning of message
        `Formatter.DEFAULT_MSG_OK_PREF`
        * Prints output to the terminal when verbosity level is set to
        `Formatter.VERBOSITY_LEVEL = Formatter.VERBOSITY_LEVELS.OK` or preceding
        level in the verbosity stack
        """
        self.fmt_print(self.oks(template, data))


    def oks(self, template, data=None):
        """Same as ok() but do not print out and return as string"""
        ok_template = '{}{}{}'.format(
            Formatter.DEFAULT_MSG_OK_COLOR,
            Formatter.DEFAULT_MSG_OK_PREF,
            template)+'{t.normal}'
        return self.fmt_to_string(ok_template, data)


    def data(self, template, data=None):
        """Formats output with fmt_to_string(template, data) and prints data with
        fmt_print()
        """
        # 3. Tamplate can be a name of Jinja2 template to load from
        #    zgcli.templates and then do the same as in 2.
        #
        # NOTE: We might need to specify which case it is explicitly as
        # detection may be junky/impossible/expensive.
        self.fmt_print(self.datas(template, data))


    def datas(self, template, data=None):
        """Same as data() but do not print out and return as string"""
        return self.fmt_to_string(template, data)


    @contextmanager
    def itemlist(self, indent=DEFAULT_INDENT, **kwargs):
        """Context manager which modifies behavior of fmt_to_string() method
        by adding extra prefix `Formatter.DEFAULT_ITEMLIST_PREF` and overrides indent
        in fmt_print() method

        :param indent: Specify output indent, defaults to `Formatter.DEFAULT_INDENT`
        :type indent: int, optional
        """
        fmt_to_string = self.fmt_to_string
        fmt_print = self.fmt_print

        @wraps(fmt_to_string)
        def wrapped_fmt_to_string(*args, **kwargs):
            return fmt_to_string(*args, prefix=Formatter.DEFAULT_ITEMLIST_PREF, **kwargs)

        @wraps(fmt_print)
        def wrapper_fmt_print(*args, **kwargs):
            return fmt_print(*args, indent=indent, **kwargs)

        self.fmt_to_string = wrapped_fmt_to_string
        self.fmt_print = wrapper_fmt_print

        yield

        self.fmt_to_string = fmt_to_string
        self.fmt_print = fmt_print


    @contextmanager
    def numlist(self, indent=DEFAULT_INDENT, **kwargs):
        """Context manager which modifies behavior of fmt_to_string() method
        by adding extra template of the prefix `Formatter.DEFAULT_NUMLIST_PREF`
        which is filled with a number of recent method's calls count and
        overrides indent in fmt_print() method

        :param indent: Specify output indent, defaults to `Formatter.DEFAULT_INDENT`
        :type indent: int, optional
        """
        fmt_to_string = self.fmt_to_string
        fmt_print = self.fmt_print

        @wraps(fmt_to_string)
        def wrapped_fmt_to_string(*args, **kwargs):
            wrapped_fmt_to_string.num_calls += 1
            prefix = Formatter.DEFAULT_NUMLIST_PREF % wrapped_fmt_to_string.num_calls
            return fmt_to_string(*args, prefix=prefix, **kwargs)
        wrapped_fmt_to_string.num_calls = 0

        @wraps(fmt_print)
        def wrapper_fmt_print(*args, **kwargs):
            return fmt_print(*args, indent=indent, **kwargs)

        self.fmt_to_string = wrapped_fmt_to_string
        self.fmt_print = wrapper_fmt_print

        yield

        self.fmt_to_string = fmt_to_string
        self.fmt_print = fmt_print


    def fmt_print(self, *args, indent=DEFAULT_INDENT, **kwargs):
        """Directs output to `sys.stderr` or `sys.stderr` according to the value
        of `Formatter.STDOUT` variable

        :param indent: Specify output indent, defaults to `Formatter.DEFAULT_INDENT`
        :type indent: int, optional
        """
        output = sys.stderr
        if Formatter.STDOUT:
            output = sys.stdout
        if indent > 0:
            indent = ' ' * indent * Formatter.DEFAULT_INDENT_STEP
            print(indent, *args, file=output, **kwargs)
            return
        print(*args, file=output, **kwargs)


    def fmt_to_string(self, template, data=None, prefix=None):
        """Fills data according to the provided template, applies coloring/formatting.
        * Additional formatting is regulated by `Formatter.DEFAULT_COLORED` flag

        :param template: 1. Template can be literal string to output without any extra steps
                         2. Template can be Jinja2 + format()-able template to colorize and
                         then pass through Jinja2 and then output (data contains actual
                         values to use)
        :type template: string, :class:`Jinja2.Template`, required
        :param data: Data to fill Jinja2 template, defaults to None
        :type data: dict, optional
        :param prefix: Optional prefix at the beginning of message
        :type prefix: string, optional
        :return: Formatted string
        :rtype: string
        """
        if re.search(JINJA_TEMPLATE_REGEX, template):
            template = Template(template).render(data)
        if Formatter.DEFAULT_COLORED:
            string = template.format(t=Formatter.TERMINAL)
        else:
            string = re.sub(STRING_FORMATTING_REGEX, '', template)
        if prefix:
            string = '{}{}'.format(prefix, string)
        return string


if __name__ == '__main__':
    print("Formatter:")
    TEST_JINJA_TEMPLATE = """
    Example template:
    {% for item in range(2) %}
        {t.blue} {{item}} {{value.center(40,'#')}}
    {% endfor %}
    """

    TEST_DATA = {'value':"Some value"}

    # Formatter.VERBOSITY_LEVEL = Formatter.VERBOSITY_LEVELS.ERR
    # Formatter.STDOUT = True
    Formatter.DEFAULT_COLORED = True
    fmt = Formatter()
    fmt.info('msg info {t.blue}{t.underline} blue underline{t.normal}')
    fmt.warn('msg warn {t.red}{t.bold}red bold{t.normal}')
    fmt.err(TEST_JINJA_TEMPLATE, TEST_DATA)
    fmt.ok('msg ok')
    fmt.data('msg data')

    Formatter.set_force_colored(True)
    Formatter.DEFAULT_COLORED = False

    fmt_2 = Formatter()
    fmt_2.info('msg info {t.blue}{t.underline} blue underline{t.normal}')
    fmt_2.warn('msg warn {t.red}{t.bold}red bold{t.normal}')
    fmt_2.err(TEST_JINJA_TEMPLATE, TEST_DATA)
    fmt_2.ok('msg ok')
    fmt_2.data('msg data')

    with fmt_2.itemlist(1):
        fmt_2.data("inside itemlist")
        fmt_2.ok("inside itemlist")
    fmt_2.data("outside itemlist")

    with fmt.numlist(2):
        fmt.data("inside numlist")
        fmt.ok("inside numlist")
    fmt.fmt_print("outside numlist")
