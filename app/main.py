import os
import subprocess

# List of built-in commands (for this stage: type, echo, exit)
BUILTINS = ["echo", "exit", "type"]

def handle_type_command(command_name):
    """Handles the 'type' command and checks if it's a builtin or executable in PATH"""
    if command_name in BUILTINS:
        print(f"{command_name} is a shell builtin")
    else:
        # Check if it's an executable in the PATH
        path_dirs = os.environ.get("PATH", "").split(":")
        found = False
        for directory in path_dirs:
            command_path = os.path.join(directory, command_name)
            if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
                print(f"{command_name} is {command_name}")
                found = True
                break
        if not found:
            print(f"{command_name}: not found")

def handle_external_program(parts):
    """Handles running an external program and printing the output as required"""
    path_dirs = os.environ.get("PATH", "").split(":")
    found = False
    for directory in path_dirs:
        command_path = os.path.join(directory, parts[0])
        if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
            # Print the program name and arguments in the required format
            print(f"Program was passed {len(parts)} args (including program name).")
            print(f"Arg #0 (program name): {parts[0]}")  # Print the program name
            for i, arg in enumerate(parts[1:], start=1):
                print(f"Arg #{i}: {arg}")
            # Run the program with arguments and capture the output
            result = subprocess.run([command_path] + parts[1:], capture_output=True, text=True)
            print(result.stdout.strip())  # Output from the external program (signature)
            found = True
            break

    if not found:
        print(f"{parts[0]}: command not found")

def main():
    while True:
        command = input("$ ").strip()  # Get the user input
        parts = command.split()  # Split the command into parts

        # Exit condition
        if command == "exit 0":
            return 0

        if len(parts) == 0:
            continue  # Skip empty input

        # Handle 'type' command
        if parts[0] == "type":
            if len(parts) > 1:
                handle_type_command(parts[1])  # Handle 'type' for a specific command
            else:
                print("type: missing operand")

        # Handle external commands
        elif parts[0] == "echo":
            print(" ".join(parts[1:]))  # Print everything after 'echo'

        else:
            handle_external_program(parts)  # Handle unknown commands (external programs)

if __name__ == "__main__":
    main()
