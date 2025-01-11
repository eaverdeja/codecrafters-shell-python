import sys
import os
import subprocess


def locate_executable(command):
    path = os.environ.get("PATH", "")
    for directory in path.split(os.pathsep):
        file_path = os.path.join(directory, command)

        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path


def handle_type(args):
    word = args[0]

    if word in builtins:
        print(f"{word} is a shell builtin")
        return

    if executable := locate_executable(word):
        print(f"{word} is {executable}")
        return

    print(f"{word}: not found")


def handle_echo(args):
    words = args[0:]
    print(" ".join(words))


def handle_exit(args):
    sys.exit(int(args[0]) if args else 0)


builtins = {
    "echo": handle_echo,
    "exit": handle_exit,
    "type": handle_type,
}


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command, *args = input().split(" ")

        if command in builtins:
            builtins[command](args)
            continue
        elif executable := locate_executable(command):
            subprocess.run([command, *args])
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
