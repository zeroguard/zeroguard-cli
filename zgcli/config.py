"""."""
from box import Box


DEFAULTS = {
    'display': {
        'max_content_width': 120,
        'output_format': 'text',
        'acceptable_output_formats': [
            'csv',
            'json',
            'tree',
            'text',
            'yaml'
        ]
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

    @staticmethod
    def create_from_defaults():
        """."""
        return Config(DEFAULTS)
