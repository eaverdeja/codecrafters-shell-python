import sys
import os
import subprocess
import shlex


def locate_executable(command):
    path = os.environ.get("PATH", "")
    for directory in path.split(os.pathsep):
        file_path = os.path.join(directory, command)

        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path


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
    tokens = shlex.split(" ".join(args))
    out.write(" ".join(tokens) + "\n")


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


def handle_redirects(args):
    out, err = sys.stdout, sys.stderr
    if "2>" in args:
        idx = args.index("2>")
        args, file_name = args[:idx], args[idx + 1]
        err = open(file_name, "w+")
    elif "1>" in args or ">" in args:
        idx = args.index("1>") if "1>" in args else args.index(">")
        args, file_name = args[:idx], args[idx + 1]
        out = open(file_name, "w+")

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

        command, *args = input().split(" ")

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
