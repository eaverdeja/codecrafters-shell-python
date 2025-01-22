import sys
import subprocess
import shlex

from .handlers import builtins
from .utils import locate_executable


def handle_redirects(args):
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


def cleanup_redirects(out, err):
    if out.fileno != sys.stdout.fileno:
        out.close()
    if err.fileno != sys.stderr.fileno:
        err.close()


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command, *args = shlex.split(input())

        args, out, err = handle_redirects(args)

        if command in builtins:
            builtins[command](args, out=out)
        elif locate_executable(command):
            subprocess.run([command, *args], stdout=out, stderr=err)
        else:
            out.write(f"{command}: command not found\n")

        cleanup_redirects(out, err)


if __name__ == "__main__":
    main()
