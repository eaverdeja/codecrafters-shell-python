import os
import sys

from .utils import locate_executable


def handle_type(args, out):
    command = args[0]

    if command in builtins:
        out.write(f"{command} is a shell builtin\n")
        return

    if executable := locate_executable(command):
        out.write(f"{command} is {executable}\n")
        return

    out.write(f"{command}: not found\n")


def handle_echo(args, out):
    out.write(" ".join(args) + "\n")


def handle_exit(args, out):
    sys.exit(int(args[0]) if args else 0)


def handle_pwd(args, out):
    out.write(os.getcwd() + "\n")


def handle_cd(args, out):
    path = str(args[0]).replace("~", os.environ.get("HOME", ""))
    try:
        os.chdir(path)
    except FileNotFoundError as e:
        out.write(f"cd: {path}: {e.strerror}\n")


builtins = {
    "echo": handle_echo,
    "exit": handle_exit,
    "type": handle_type,
    "pwd": handle_pwd,
    "cd": handle_cd,
}
