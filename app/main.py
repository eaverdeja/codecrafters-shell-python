import sys
import os

BUILTIN_COMMANDS = [
    "echo",
    "exit",
    "type",
]

def list_executables(path):
    executables = []
    if os.path.exists(path) and os.path.isdir(path):
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            # Check if file is executable
            if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                executables.append(file)
    return executables


def main():
    sys.stdout.write("$ ")
    
    command = input()
     
    pieces = command.split(" ")
    match pieces[0]:
        case "type":
            word = pieces[1]
            if word in BUILTIN_COMMANDS:
                sys.stdout.write(f"{word} is a shell builtin\n")
            else:
                path_list = os.environ['PATH'].split(os.pathsep)
                path_for_word = None
                for path in path_list:
                    executables = list_executables(path)
                    if word in executables:
                        path_for_word = path + f"/{word}"
                
                if path_for_word:
                    sys.stdout.write(f"{word} is {path_for_word}\n")
                else:
                    sys.stdout.write(f"{word}: not found\n")
        case "echo":
            words = pieces[1:]
            sys.stdout.write(" ".join(words) + "\n")
        case "exit":
            sys.exit(0)
        case _:
            sys.stdout.write(f"{command}: command not found\n")
            
    return main()


if __name__ == "__main__":
    main()
