import sys
import subprocess
import shlex
import logging

from .autocomplete import Autocompleter
from .handlers import builtins
from .utils import locate_executable, setup_logging


def _handle_redirects(args):
    out, err = sys.stdout, sys.stderr

    redirects = {
        "2>": (2, "w"),
        "2>>": (2, "a"),
        "1>>": (1, "a"),
        ">>": (1, "a"),
        "1>": (1, "w"),
        ">": (1, "w"),
    }

    for operator, (file_descriptor, mode) in redirects.items():
        if operator in args:
            idx = args.index(operator)
            args, file_name = args[:idx], args[idx + 1]

            if file_descriptor == 1:
                out = open(file_name, mode)
            else:
                err = open(file_name, mode)
            break

    return args, out, err


def _cleanup_redirects(out, err):
    if out.fileno != sys.stdout.fileno:
        out.close()
    if err.fileno != sys.stderr.fileno:
        err.close()


def _run(_logger: logging.Logger):
    sys.stdout.write("$ ")
    sys.stdout.flush()

    command, *args = shlex.split(input())

    args, out, err = _handle_redirects(args)

    if command in builtins:
        builtins[command](args, out=out)
    elif locate_executable(command):
        subprocess.run([command, *args], stdout=out, stderr=err)
    else:
        out.write(f"{command}: command not found\n")

    _cleanup_redirects(out, err)


def main():
    # Using print statements to debug this challenge is not practical,
    # so we should log to an external file for debugging purposes
    try:
        logger = setup_logging()
    except FileNotFoundError:
        # Running in CI
        logger = logging.Logger("codecrafters shell")

    # Sets up autocompletion
    Autocompleter(out=sys.stdout, logger=logger)

    # Main loop
    try:
        while True:
            _run(logger)
    except KeyboardInterrupt:
        sys.stdout.write("Closing...")
        sys.stdout.flush()
        sys.stdout.close()


if __name__ == "__main__":
    main()
