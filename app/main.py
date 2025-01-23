import sys

# sys.stdout.write("$ ")

def main():
    while True:  # Use a loop to keep the program running until 'exit 0' is entered
        command = input("$ echo ")
        if command == "exit 0":
            return 0  # Exit the program

        #print(f"{command}: command not found")
        print(f"{command}")

if __name__ == "__main__":
    main()
