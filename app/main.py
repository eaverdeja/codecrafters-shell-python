import sys


def main():
    sys.stdout.write("$ ")
    
    command = input()
     
    pieces = command.split(" ")
    match pieces[0]:
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
