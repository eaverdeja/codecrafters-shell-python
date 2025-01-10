import sys


def main():
    sys.stdout.write("$ ")
    
    # Wait for user input
    command = input()
     
    is_invalid_command = True
    if is_invalid_command:
        sys.stdout.write(f"{command}: command not found\n")
    
    return main()


if __name__ == "__main__":
    main()
