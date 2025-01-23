import os
import subprocess

# List of built-in commands (for this stage: type, echo, exit, pwd, cd)
BUILTINS = ["echo", "exit", "type", "pwd", "cd"]

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
                print(f"{command_name} is {command_path}")  # Print the full path
                found = True
                break
        if not found:
            print(f"{command_name}: not found")

def handle_external_program(parts):
    """Handles running an external program and printing the output as required"""
    command_name = parts[0]  # The name of the command (e.g., custom_exe_4109)
    path_dirs = os.environ.get("PATH", "").split(":")
    found = False
    for directory in path_dirs:
        command_path = os.path.join(directory, command_name)
        if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
            # Run the program with arguments and capture the output
            result = subprocess.run([command_name] + parts[1:], capture_output=True, text=True)
            print(result.stdout.strip())  # Output from the external program (signature)
            found = True
            break

    if not found:
        print(f"{command_name}: command not found")

def handle_cd_command(path):
    """Handles the 'cd' command to change the current working directory"""
    # Replace ~ with the value of the HOME environment variable
    if path == "~":
        path = os.environ.get("HOME")
    elif path.startswith("~/"):
        path = os.path.join(os.environ.get("HOME"), path[2:])

    try:
        os.chdir(path)  # Change the directory (handles absolute, relative, and ~ paths)
    except FileNotFoundError:
        print(f"cd: {path}: No such file or directory")  # Print error if directory doesn't exist

def parse_command(command):
    """Custom command parser to handle single quotes, double quotes, backslashes, and unquoted arguments"""
    parts = []
    current_part = ""
    in_single_quotes = False
    in_double_quotes = False
    escape_next = False

    for char in command:
        if escape_next:
            # If the next character is escaped, add it to the current part
            current_part += char
            escape_next = False
        elif char == "\\":
            # If a backslash is encountered, escape the next character
            escape_next = True
        elif char == "'" and not in_double_quotes:
            # Toggle single quotes
            in_single_quotes = not in_single_quotes
        elif char == '"' and not in_single_quotes:
            # Toggle double quotes
            in_double_quotes = not in_double_quotes
        elif char.isspace() and not (in_single_quotes or in_double_quotes):
            # If a space is encountered outside quotes, finalize the current part
            if current_part:
                parts.append(current_part)
                current_part = ""
        else:
            # Add the character to the current part
            current_part += char

    # Add the last part if it exists
    if current_part:
        parts.append(current_part)

    return parts

def main():
    while True:
        command = input("$ ").strip()  # Get the user input

        # Exit condition
        if command == "exit 0":
            return 0

        if len(command) == 0:
            continue  # Skip empty input

        # Parse the command into parts, handling quotes and backslashes
        parts = parse_command(command)

        # Handle 'type' command
        if parts[0] == "type":
            if len(parts) > 1:
                handle_type_command(parts[1])  # Handle 'type' for a specific command
            else:
                print("type: missing operand")

        # Handle 'pwd' command
        elif parts[0] == "pwd":
            print(os.getcwd())  # Print the current working directory

        # Handle 'cd' command
        elif parts[0] == "cd":
            if len(parts) > 1:
                handle_cd_command(parts[1])  # Handle 'cd' with the provided path
            else:
                # If no path is provided, default to the home directory
                handle_cd_command("~")

        # Handle 'echo' command
        elif parts[0] == "echo":
            print(" ".join(parts[1:]))  # Print everything after 'echo'

        # Handle external commands
        else:
            handle_external_program(parts)  # Handle unknown commands (external programs)

if __name__ == "__main__":
    main()