"""."""
import logging
import os
import platform

from box import Box, BoxKeyError


DEFAULTS = {
    'display': {
        'max_content_width': 120
    },

    'internal': {
        'default_user_config_path': '~/.config/zg/config.yml',
        'default_user_config_path_darwin': '~/config/zg/config.yml',
        'default_user_config_path_linux': '~/config/zg/config.yml',
        'default_user_config_path_windows': '%USERPROFILE%/.zg/config.yml',

        'default_log_format': 'native',
        'acceptable_log_formats': ['native', 'jsonl', 'syslog']
    }
}


class Config(Box):
    """."""

    PLATFORM = platform.system().lower()

    @staticmethod
    def create_from_defaults():
        """."""
        return Config(DEFAULTS)

    def get_default_user_config_path(self):
        """Get expanded and OS-specific default user configuration path.

        :return: Default user configuration file path specific to current
                 operating system user and system type.
        :rtype:  str
        """
        try:
            path = self.internal['default_user_config_path_%s' % self.PLATFORM]
        except BoxKeyError:
            path = self.internal.default_user_config_path

        return os.path.expanduser(path)
