ZeroGuard CLI
=============
> NOTE: This is an initial CLI application layout draft. It will be later
> removed completely or moved to Wiki / ReadTheDocs.

CLI Structure
-------------
### `zg` | Root Command Options
#### Flags
* `-L --log` - Enable logging
* `-S --log-stdout` - Send log messages to STDOUT instead of STDERR if logging
  is enabled.
* `-C --no-config` - Ignore configuration file even if it exists
* `-h --help` - Print help message and exit
* `-q --quiet` - Do not output any informational messages
* `-v -V --version` - Print ZG CLI version and exit

#### Options With Arguments
* `-l --log-level <LEVEL> [default: warning]` - Logging level
  - `debug, dbg`
  - `info, inf`
  - `warning, warn`
  - `error, err`
  - `critical, crit`
* `-F --log-format <LOG_FORMAT> [default: default]` - Logging format
  - `default` - Default logging format (format is hard coded into the
    application)
  - `jsonl` - JSON list: each log message is a JSON object
  - `syslog` - [RFC5424](https://tools.ietf.org/html/rfc5424#section-6)
    compatible logging format
* `-f --format <FORMAT> [default: verbose]` - Output format
  - `csv`
  - `json`
  - `tree` - Format similar to output of `tree` \*nix command
  - `verbose, verb` - Human friendly plain text output format
  - `yaml`
* `-c --config <PATH> [default: ~/.config/zg/config]` - Path to ZG
  configuration file. Specify `-` as a path to read from STDIN.
* `-i --identity <PATH> [default: ~/.config/zg/identity]` - Path to ZG identity
  file (file where authentication token is stored after initial `zg login`).
  Specify `-` as a path to read from STDIN.

### `zg status` | Status Command
Output ZeroGuard systems status and health information

Conventions & Resources
-----------------------
* https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html
* https://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Options.html
* https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html
* https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html
* https://www.math.uni-hamburg.de/doc/java/tutorial/essential/attributes/_posix.html
