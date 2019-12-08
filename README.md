ZeroGuard CLI
=============
> NOTE: This is an initial CLI application layout draft. It will be later
> removed completely or moved to Wiki / ReadTheDocs.

CLI Structure
-------------
### Root Command Options
* `--log | --no-log [default: --no-log]` - Enable or disable logging
* `--log-stdout | --log-stderr [default: --log-stderr]` - Stream to which log
  messages will be sent (if logging is enabled).
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
* `--no-config` - Ignore configuration file even if it exists
* `-i --identity <PATH> [default: ~/.config/zg/identity]` - Path to ZG identity
  file (file where authentication token is stored after initial `zg login`).
  Specify `-` as a path to read from STDIN.
* `-h --help` - Print help message and exit
* `-v -V --version` - Print ZG CLI version and exit

### Help Command
`zg help` is an alias of `zg -h`

### Version Command
`zg version` is an alias of `zg -v`

Conventions & Resources
-----------------------
* https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html
* https://www.gnu.org/software/libc/manual/html_node/Getopt-Long-Options.html
* https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html
* https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html
* https://www.math.uni-hamburg.de/doc/java/tutorial/essential/attributes/_posix.html
