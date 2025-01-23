import sys
import os
import subprocess

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
                
                # First, check if it's a built-in command
                if cmd_to_check in SHELL_BUILTINS:
                    print(f"{cmd_to_check} is a shell builtin")
                else:
                    # Check if the command is an executable file in the PATH
                    path_dirs = os.environ.get("PATH", "").split(":")
                    found = False
                    
                    for dir in path_dirs:
                        command_path = os.path.join(dir, cmd_to_check)
                        if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
                            # Use just the executable name, not the full path
                            print(f"{cmd_to_check} is {cmd_to_check}")
                            found = True
                            break
                    
                    if not found:
                        print(f"{cmd_to_check}: not found")
            else:
                print("type: missing operand")  # Handle missing operand for `type`
        
        # Handle the `echo` command
        elif parts[0] == "echo":
            # Print everything after "echo"
            print(" ".join(parts[1:]))
        
        # Handle unrecognized commands
        else:
            # Check if it's an executable and run it
            path_dirs = os.environ.get("PATH", "").split(":")
            found = False
            
            for dir in path_dirs:
                command_path = os.path.join(dir, parts[0])
                if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
                    # Extract the base name of the command (without the path)
                    command_name = os.path.basename(command_path)
                    
                    # Execute the program with arguments
                    try:
                        result = subprocess.run([command_path] + parts[1:], capture_output=True, text=True)
                        # Print output from the program
                        output = result.stdout.strip()  # Ensure no extra newlines or spaces
                        print(f"Arg #0 (program name): {command_name}")  # Print just the executable name
                        print(f"Arg #1: {parts[1]}")  # Print the first argument
                        print(output)  # Print the output directly
                    except Exception as e:
                        print(f"Error running the command: {e}")
                    found = True
                    break
            
            if not found:
                print(f"{command}: command not found")

if __name__ == "__main__":
    main()
