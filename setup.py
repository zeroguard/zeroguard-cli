#!/usr/bin/env python3
"""ZeroGuard CLI package build script."""
import json
import os
from setuptools import setup, find_packages

import zgcli


LOCK_FILE = 'Pipfile.lock'
README_FILE = 'README.md'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ABOUT_FILE = os.path.join(BASE_DIR, 'zgcli', '__version__.py')


def parse_requirements(lock_fpath):
    """Parse requirements and test requirements from a given Pipfile.lock.

    :return: Requirements and test requirements usable by setup function.
    :rtype:  2-tuple of list(str)
    """
    with open(lock_fpath) as lock_file:
        lock_deps = json.load(lock_file)

    return (
        ['%s%s' % (k, v['version']) for k, v in lock_deps['default'].items()],
        ['%s%s' % (k, v['version']) for k, v in lock_deps['develop'].items()]
    )


def main():
    """Set up the package."""
    # Load README.md file content
    with open(README_FILE) as readme_file:
        readme = readme_file.read()

    # Parse out requirements from Pipfile.lock
    requirements, test_requirements = parse_requirements(LOCK_FILE)

    # Setup the package
    setup(
        name=zgcli.__title__,
        version=zgcli.__version__,
        license=zgcli.__license__,

        description=zgcli.__description__,
        long_description=readme,
        long_description_content_type='text/markdown',

        author=zgcli.__author__,
        author_email=zgcli.__author_email__,
        url=zgcli.__home_url__,

        packages=find_packages(),
        package_data={'': ['CHANGELOG.md', 'LICENSE']},
        entry_points={'console_scripts': ['zg=zgcli.main:main']},

        python_requires='>=3.5',
        install_requires=requirements,
        tests_require=test_requirements,

        classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Console',
            'Intended Audience :: Information Technology',
            'License :: OSI Approved :: GNU Affero General Public License v3',
            'Natural Language :: English',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Topic :: Security'
        ],

        project_urls={
            'Documentation': zgcli.__docs_url__,
            'Source': zgcli.__source_url__
        }
    )


if __name__ == '__main__':
    main()
