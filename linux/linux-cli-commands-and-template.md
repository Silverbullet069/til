# Linux CLI templates

<!-- tl;dr starts -->

There are a lot of useful CLI commands and templates that I would like to archive for later use. Later, it's better to add the CLI commands into [`tealdeer-rs/tealdeer`](https://github.com/tealdeer-rs/tealdeer) or use Fish history or Bash history `tac ~/.bash_history | grep "pattern" | less`

<!-- tl;dr ends -->

## Differences between `curl -o [FILE]` and `curl > [FILE]`:

| Features                                 | `curl -o [FILE]` | `curl > [FILE]` |
| ---------------------------------------- | ---------------- | --------------- |
| Built-in?                                | Yes              | No, shell       |
| Create parent directories?               | Yes              | No              |
| Retain file's permission and timestamps? | Yes              | No, umask       |
| Clean leftover files if download failed? | Yes              | No              |

## Run a command against a set of files

`find -print0` outputs the names of found files separated by ASCII NULL character, instead of newlines. This is useful when handling filenames that contain spaces, newlines, ... whitespaces in general.

`xargs -0` safely process filename with special character by parsing them using ASCII NULL

```sh
find /path/to/search -name "[PATTERN]" -print0 | xargs -0 COMMAND
```

## Initial CLI options

```sh
while [ -n "$1" ]
do
  case "$1" in
    "-a")
      shift
      OPT_FOO=1
      ;;
    "-b")
      shift
      OPT_BAR=1
      ;;
    # ... more options here
    *)
      echo "Unrecognized option: $1"
      shift
      OPT_SHOWHELP=1
      ;;
  esac
done
```

## Show help

```sh
if [ -n "$OPT_SHOWHELP" ]
then
  echo
  echo "USAGE: $(basename "$0") [-a] [-b]"
  echo
  echo "     -a blah blah blah"
  echo "     -b bloo bloo bloo"
  echo
  exit 1
fi
```

## Check dependency

```sh
# redirect both stdout and stderr to /dev/null
# suppress all possible output
if ! which jq &>/dev/null
then
  echo "The 'jq' utility is required"
  echo "    Most package managers should have a 'jq' package available"
  EXIT=1
fi

# ... more dependencies check
```

## Extract the directory that contains the script via script name

`dirname "$(realpath "$(which "$0")")"`

## Heredoc

```sh
cat << EOF > "/your/path/to/file"
blah
blah
blah
...
blah
EOF
```

## Fetch -> Temp -> New file

```sh
curl ...
if [ ... ]
then
	echo "Error, save to .temp"
	exit 1
else
	# write from .temp to new file
fi
```

## Short-circuit

```sh
[COMMAND THAT CAN BE FAILED] || exit 1
```

## Logging system

```sh
#!/bin/sh

# Colors
readonly RED='\033[0;31m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly GRAY='\033[0;37m'
readonly GREEN='\033[0;32m'
readonly NC='\033[0m'

# Format settings
readonly TIME_FORMAT='%Y-%m-%d %H:%M:%S'
# %b: ARGUMENT as a string with '\' escapes interpreted, except that octal escapes are of the form \0 or \0NNN
# Cre: https://stackoverflow.com/a/5412825
readonly LOG_FORMAT='%-19s %s: [%b%-5s%b] %s\n'

log() {
    local level=$1; shift
    local color=$1; shift
    local timestamp=$(date +"$TIME_FORMAT")
    local script_name=$(basename "$0")
    # local line_num=${BASH_LINENO[0]}

    printf "$LOG_FORMAT" \
        "$timestamp" \
        "$script_name" \
        "$color" "$level" "$NC" \
        "$*"
}

error()   { log "ERROR" "$RED" "$@" >&2; }
warning() { log "WARN" "$YELLOW" "$@" >&2; }
info()    { log "INFO" "$BLUE" "$@"; }
debug()   { [ "${DEBUG:-0}" -eq 1 ] && log "DEBUG" "$GRAY" "$@" >&2 || return 0; }
success() { log "SUCC" "$GREEN" "$@"; }
```
