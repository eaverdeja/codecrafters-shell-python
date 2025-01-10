import sys

BUILTIN_COMMANDS = [
    "echo",
    "exit",
    "type",
]

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
