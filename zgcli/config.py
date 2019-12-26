"""."""
from box import Box


DEFAULTS = {
    'display': {
        'output_format': 'text',
        'acceptable_output_formats': [  # FIXME: Read-only
            'csv',
            'json',
            'text',
            'tree',
            'yaml'
        ],

        # Whether to colorize CLI output. Force coloring means that output will
        # be colored even if redirected and/or piped by a user.
        'force_colored': False,
        'colored': True,

        'max_content_width': 120,
    },

    'logging': {
        'log_format': 'native',
        'acceptable_log_formats': [  # FIXME: Read-only
            'native',
            'jsonl',
            'syslog'
        ],

        'log_level': 'info',
        'acceptable_log_levels': [  # FIXME: Read-only
            'debug',
            'info',
            'warning',
            'critical'
        ],
    },

    'api': {
        'endpoint': 'api.zeroguard.com',

        # FIXME: All view-related schemas should be moved somewhere else down
        # the road. Probably as soon as we get SDK implemented.
        # FIXME: Read-only
        'data_groups': [
            'dns',
            'har',
            'ports',
            'ssl',
            'track'
            'whois'
        ],

        # FIXME: Read-only
        'per_group_views': [
            'all',
            'summary'
        ],

        # FIXME: Read-only
        'compound_views': [
            'all',
            'summary'
        ]
    }
}


class Config(Box):
    """."""

    @staticmethod
    def create_from_defaults():
        """."""
        return Config(DEFAULTS)


# Create a singletone default configuration instance
DEFAULT_CONFIG = Config.create_from_defaults()
