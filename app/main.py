import os
import subprocess
import shlex

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
    """Parses the command into parts, handling single and double quotes"""
    lexer = shlex.shlex(command, posix=True)
    lexer.whitespace_split = True
    lexer.quotes = '"'  # Treat double quotes as quoting characters
    lexer.whitespace = ' \t\n'  # Treat spaces, tabs, and newlines as whitespace
    parts = list(lexer)

    # Remove single quotes from the parsed parts
    for i, part in enumerate(parts):
        if part.startswith("'") and part.endswith("'"):
            parts[i] = part[1:-1]  # Remove the single quotes

    return parts

def main():
    while True:
        command = input("$ ").strip()  # Get the user input

        # Exit condition
        if command == "exit 0":
            return 0

        if len(command) == 0:
            continue  # Skip empty input

        # Parse the command into parts, handling single and double quotes
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