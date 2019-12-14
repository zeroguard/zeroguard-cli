#!/usr/bin/env bash
#
###############################################################################
# Title:       invoke.sh
# Description: Wrapper around zg CLI application to run it without installing
#              as a package or generating a binary. Convenience script only and
#              should not be a way to get zg running on user's host.
# Usage:       invoke.sh ZG_CLI_OPTIONS_HERE
set -euo pipefail
pipenv run python3 -m zgcli.main "$@"
