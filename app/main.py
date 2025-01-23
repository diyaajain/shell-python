import sys

# List of shell builtins
SHELL_BUILTINS = ["echo", "exit", "type"]

def main():
    while True:
        command = input("$ ")
        
        if command == "exit 0":
            return 0  # Exit the program
        
        parts = command.split()  # Split the input into words
        
        # Check if the command is 'type'
        if parts[0] == "type":
            if len(parts) > 1:
                cmd_to_check = parts[1]
                if cmd_to_check in SHELL_BUILTINS:
                    print(f"{cmd_to_check} is a shell builtin")
                else:
                    print(f"{cmd_to_check}: not found")
            else:
                print("type: missing operand")
        
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
