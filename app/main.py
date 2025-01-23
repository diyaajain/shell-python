import sys

def main():
    while True:  # Use a loop to keep the program running until 'exit 0' is entered
        sys.stdout.write("$ ")

        command = input()

        if command == "exit 0":
            return 0  # Exit the program

        print(f"{command}: command not found")
        main()

if __name__ == "__main__":
    main()
