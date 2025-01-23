import sys

# List of shell builtins
SHELL_BUILTINS = ["echo", "exit", "type"]

def main():
    while True:
        command = input("$ ")
        
        # Exit condition
        if command == "exit 0":
            return 0

        # Split the command into parts
        parts = command.split()

        # Handle the `type` command
        if parts[0] == "type":
            if len(parts) > 1:  # Check if an argument is provided
                cmd_to_check = parts[1]
                if cmd_to_check in SHELL_BUILTINS:
                    print(f"{cmd_to_check} is a shell builtin")
                else:
                    print(f"{cmd_to_check}: not found")
            else:
                print("type: missing operand")  # Handle missing operand for `type`
        
        # Handle the `echo` command
        elif parts[0] == "echo":
            # Print everything after "echo"
            print(" ".join(parts[1:]))
        
        # Handle unrecognized commands
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
