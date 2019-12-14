"""Output formatter module."""
from contextlib import contextmanager
import logging

# TODO: These libraries should provide low level building blocks for this
# module. Feel free to add other dependencies if required but please make sure
# we avoid adding a lot of "convenience" libraries if that can be easily
# implemented with what we already have in place.
import blessings
import colorama
import jinja2


# NOTE: Do we want to inherit from logger? In a perfect world we'd want to,
# because that would allow us to get levels OOTB and easily conditionally
# disabled some messages.
#
# Again, this is a module for formatting CLI application output, not outputting
# logs. We will still have an ability to enable logging from CLI, but that is
# mostly for debugging how SDK and CLI work together. Logging and output
# produced by formatter should be completely independent.
class Formatter(logging.Logger):
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
    DEFAULT_MSG_ERR_COLOR = ''  # Red

    DEFAULT_MSG_INFO_PREF = '---(i) INFO: '
    DEFAULT_MSG_INFO_COLOR = ''  # White

    DEFAULT_MSG_OK_PREF = '---(+) OK: '
    DEFAULT_MSG_OK_COLOR = ''  # Green

    DEFAULT_MSG_WARN_PREF = '---(!) WARN: '
    DEFAULT_MSG_WARN_COLOR = ''  # Orange

    DEFAULT_ITEMLIST_PREF = '* '
    DEFAULT_NUMLIST_PREF = '%i. '

    # NOTE: Preffer tabs over spaces for formatting. This will make it easier
    # to cut and sed output of your CLI. See if you can make tab to look like 2
    # spaces on CLI.
    DEFAULT_INDENT = 0
    DEFAULT_INDENT_STEP = 2

    # NOTE: Allow to output all messages to STDOUT
    DEFAULT_FD = ''  # STDERR

    # NOTE: Output in color by default, unless output is redirected
    DEFAULT_COLORED = True

    # NOTE: Allow to force color even if redirected
    DEFAULT_FORCE_COLORED = False


    def __init__(self, **kwargs):
        """."""

    def info(self, template, data=None):
        """."""
        # 1. Template can be literal string to output without any extra steps
        # 2. Template can be Jinja2 + format()-able template to colorize and
        #    then pass through Jinja2 and then output (data contains actual
        #    values to use)
        # 3. Tamplate can be a name of Jinja2 template to load from
        #    zgcli.templates and then do the same as in 2.
        #
        # NOTE: We might need to specify which case it is explicitly as
        # detection may be junky/impossible/expensive.

    def infos(self, template, data=None):
        """Same as info() but do not print out and return as string."""

    def warn(self, template, data=None):
        """."""

    def warns(self,template, data=None):
        """."""

    def err(self, template, data=None):
        """."""

    def errs(self, template, data=None):
        """."""

    def ok(self, template, data=None):
        """."""

    @contextmanager
    def itemlist(self, **kwargs):
        """."""

    @contextmanager
    def numlist(self, **kwargs):
        """."""

    # NOTE: And a lot of other methods ...
