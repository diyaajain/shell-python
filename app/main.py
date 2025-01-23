import sys

def main():
    while True:  # Use a loop to keep the program running until 'exit 0' is entered
        command = input("$ ")
        if command == "exit 0":
            return 0  # Exit the program

        # Split the command into words
        parts = command.split()

        # Handle the `echo` command
        if parts[0] == "echo":
            # Join and print everything after "echo"
            print(" ".join(parts[1:]))
        else:
            # Handle unknown commands
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
