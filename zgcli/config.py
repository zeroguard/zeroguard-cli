"""."""
import os
import platform

from box import Box, BoxKeyError


DEFAULTS = {
    'display': {
        'max_content_width': 120,
        'format': 'verbose',
        'acceptable_formats': [
            'csv',
            'json',
            'tree',
            'verbose',
            'yaml'
        ]
    },

    'internal': {
        'user_config_path': '~/.config/zg/config.yml',
        'user_config_path_darwin': '~/.config/zg/config.yml',
        'user_config_path_linux': '~/.config/zg/config.yml',
        'user_config_path_windows': '%USERPROFILE%/.zg/config.yml',

        'user_identity_path': '~/.config/zg/identity',
        'user_identity_path_darwin': '~/.config/zg/identity',
        'user_identity_path_linux': '~/.config/zg/identity',
        'user_identity_path_windows': '%USERPROFILE%/.zg/identity'
    },

    'logging': {
        'log_format': 'native',
        'acceptable_log_formats': [
            'native',
            'jsonl',
            'syslog'
        ],

        'log_level': 'info',
        'acceptable_log_levels': [
            'debug',
            'info',
            'warning',
            'critical'
        ],
    }
}


class Config(Box):
    """."""

    PLATFORM = platform.system().lower()

    @staticmethod
    def create_from_defaults():
        """."""
        return Config(DEFAULTS)

    def get_user_config_path(self):
        """Get expanded and OS-specific path to user configuration file.

        :return: Path to a user configuration file specific to current
                 operating system user and system type.
        :rtype:  str
        """
        try:
            path = self.internal['user_config_path_%s' % self.PLATFORM]
        except BoxKeyError:
            path = self.internal.user_config_path

        return os.path.expanduser(path)

    def get_user_identity_path(self):
        """Get expanded and OS-specific path to user identity file.

        :return: Path to user identity file path specific to current operating
                 system user and system type.
        :rtype:  str
        """
        try:
            path = self.internal['user_identity_path_%s' % self.PLATFORM]
        except BoxKeyError:
            path = self.internal.user_identity_path

        return os.path.expanduser(path)
