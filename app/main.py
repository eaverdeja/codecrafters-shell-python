import sys


def main():
    sys.stdout.write("$ ")
    
    command = input()
     
    pieces = command.split(" ")
    match pieces[0]:
        case "exit":
            sys.exit(0)
        case _:
            sys.stdout.write(f"{command}: command not found\n")
            
    return main()


if __name__ == "__main__":
    main()
