import sys

def main():
    while True:
        command = input("$ ")
        
        # Exit condition
        if command == "exit 0":
            return 0

        # Split the command into parts
        parts = command.split()

        # Handle the `echo` command
        if parts[0] == "echo":
            # Print everything after "echo"
            print(" ".join(parts[1:]))
        else:
            # Handle unknown commands
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
