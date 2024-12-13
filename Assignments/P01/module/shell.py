import sys, os
from getch import Getch
from cmd_pkg import pwd, touch, cd, ls, mkdir, user_login, echo, rm, rmdir, cat_read, cat_write, save_command_to_history, history, head, tail, cp, mv, grep, chmod, wc, man, less, more, sort
from cmd_pkg.exe_cmd_by_num import exe_cmd_by_num, get_user_history

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import load_config, save_config

# Creating an instance of our Getch class
getch = Getch()

# Initialize configuration
def initialize_shell():
    global config, current_directory, command_history, history_index, prompt
    config = load_config()
    current_directory = config["Settings"]["current_directory"]
    prompt = "$ "  # Set default prompt

    # Fetch user history on startup
    user_history = get_user_history()
    command_history = list(user_history.values()) if isinstance(user_history, dict) else []
    history_index = len(command_history)  # Initialize history index

def update_shell_config(new_user_directory):
    """Updates the shell configuration after a user login."""
    global config, current_directory, current_user
    config["Settings"]["current_directory"] = new_user_directory
    save_config(config)
    current_directory = new_user_directory

def print_cmd(cmd):
    """Cleans the command line, then prints the prompt and the current command."""
    sys.stdout.write("\r" + " " * 80)  # Clear the current line
    sys.stdout.write("\r" + prompt + cmd)  # Print the prompt and command
    sys.stdout.flush()  # Flush output buffer

def clear_screen():
    """Clears the terminal screen."""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def parse_pipeline(cmd):
    """
    Parses a piped command into individual commands.

    Args:
        cmd (str): The entire command string.

    Returns:
        list: List of individual commands.
    """
    return [command.strip() for command in cmd.split('|')]

def execute_pipeline(cmd):
    """
    Executes piped commands in sequence.

    Args:
        cmd (str): Full command string with pipes.

    Returns:
        None
    """
    # Log the piped command into history
    save_command_to_history(cmd)

    commands = parse_pipeline(cmd)
    input_data = None  # Initial input is None (no prior command output)

    for command in commands:
        tokens = command.split()  # Tokenize the command
        cmd_name = tokens[0]
        args = tokens[1:]

        # Dispatch to the appropriate command function
        if cmd_name == "grep":
            flags = [arg for arg in args if arg.startswith("-")]  # Extract flags
            if input_data is None:
                if flags == []:
                    pattern = args[0]
                    file_name = args[1]
                else:
                    pattern = args[1]
                    file_name = args[2]
                input_data = grep(pattern, file_name=file_name, flags=flags, input_data=input_data)
            else:
                if flags == []:
                    pattern = args[0]
                else:
                    pattern = args[1]
                input_data = grep(pattern, file_name=None, flags=flags, input_data=input_data)
        elif cmd_name == "wc":
            if args[0] == "-l":
                count_type = 'lines'
            elif args[0] == "-w":
                count_type = 'words'
            elif args[0] == '-c':
                count_type = 'chars'
            if input_data is None:
                file_name = args[1]
                input_data = wc(file_name=file_name, piped_input=input_data, count_type=count_type)
            else:
                input_data = wc(file_name=None, piped_input=input_data, count_type=count_type)
        elif cmd_name == "head":
            lines = int(args[0]) if args and args[0].startswith("-") else 10
            if input_data is None:
                file_name = args[1]
                input_data = head(file_name=file_name, lines=lines, piped_input=input_data)
            else:
                lines = int(args[0][1:])
                input_data = head(file_name=None, lines=lines, piped_input=input_data)
        elif cmd_name == "tail":
            lines = int(args[0][1:]) if args and args[0].startswith("-") else 10
            if input_data is None:
                file_name = args[1]
                input_data = tail(file_name=file_name, lines=lines, piped_input=input_data)
            else:
                input_data = tail(file_name=None, lines=lines, piped_input=input_data)
        elif cmd_name == "cat":
            if input_data is None:
                file_name = args[0]
                input_data = cat_read(file_name=file_name, piped_input=input_data)
            else:
                input_data = cat_read(file_name=None, piped_input=input_data)
        elif cmd_name == "less":
            if input_data is None:
                file_name = args[0]
                input_data = less(file_name=file_name, piped_input=input_data)
            else:
                input_data = cat_read(file_name=None, piped_input=input_data)
        elif cmd_name == "more":
            if input_data is None:
                file_name = args[0]
                input_data = more(file_name=file_name, piped_input=input_data)
            else:
                input_data = cat_read(file_name=None, piped_input=input_data)
        elif command == "sort":
            flags = [arg for arg in args if arg.startswith("-")]
            if input_data is None:
                file_name = args[-1]
                input_data = sort(file_name=file_name, piped_input=None, flags=flags)
            else:
                input_data = sort(file_name=None, piped_input=input_data, flags=flags)
        elif cmd_name == "history":
            input_data = history(piped_input=input_data)
        else:
            print(f"Error: Unsupported command '{cmd_name}'.")
            return

    # Print the final output
    if input_data:
        print(input_data)

def parse_and_execute(cmd):
    """
    Parses and executes a command or a pipeline.
    Args:
        cmd (str): The full command string entered by the user.
    Returns:
        bool: Whether the shell should restart (e.g., after user login).
    """
    if cmd.strip() == "":
        return False  # Ignore empty commands

    global command_history, history_index
    
    # Handle `!command_number`
    if cmd.startswith("!"):
        try:
            command_number = int(cmd[1:])  # Extract the command number
            retrieved_command = exe_cmd_by_num(command_number)  # Fetch the command
            if retrieved_command:
                return parse_and_execute(retrieved_command)  # Recursively execute
            else:
                print(f"Error: Command not found for number {command_number}.")
        except ValueError:
            print("Error: Invalid command number format.")
        return False
    
    # Log the command to history if it's not a duplicate
    if not command_history or cmd != command_history[-1]:
        command_history.append(cmd)
        history_index = len(command_history)  # Reset the history index
        save_command_to_history(cmd)  # Save to the database

    try:
        # Check if the command involves a pipeline
        if "|" in cmd:
            execute_pipeline(cmd)  # Process piped commands
            return False

        # Split and process regular commands
        tokens = cmd.split()
        command = tokens[0]  # Extract the command name
        args = tokens[1:]  # Extract any arguments

        # Dispatch regular commands
        if command == "exit":
            sys.exit(0)
        elif command == "clear":
            clear_screen()
        elif command == "ls":
            flags = []
            for arg in args:
                if arg.startswith("-"):  # Check if the argument is a flag
                    for char in arg[1:]:  # Extract individual flags (e.g., -lh -> l, h)
                        flags.append(f"-{char}")  # Append each flag as a separate item
            ls(flags)  # Pass the parsed flags to the ls function
        elif command == "sort":
            flags = [arg for arg in args if arg.startswith("-")]
            file_name = args[-1]
            print(sort(file_name=file_name, flags= flags))  # Pass the parsed flags to the sort function

        elif command == "su" or command == "sudo":
            if len(args) > 0:
                user_login(args[0])
                initialize_shell()  # Reload the shell configuration for the new user
                print(f"Logged in as {args[0]}.")
                return True  # Signal to restart the shell after successful login
            else:
                print(f"Error: {command} requires a username.")
        elif command == "grep":
            flags = [arg for arg in args if arg.startswith("-")]  # Extract flags
            non_flag_args = [arg for arg in args if not arg.startswith("-")]  # Extract non-flag args
            if len(non_flag_args) < 2:  # Ensure at least pattern and file_name
                print("Usage: grep <pattern> <filename>")
            else:
                pattern = non_flag_args[0]
                file_name = non_flag_args[1]
                print(grep(pattern, file_name, flags))  # Execute grep and print the result
        elif command == "wc":
            if len(args) >= 1:
                if args[0] == "-l":
                    count_type = 'lines'
                elif args[0] == "-w":
                    count_type = 'words'
                elif args[0] == '-c':
                    count_type = 'chars'
                file_name = args[1]
                print(wc(file_name = file_name, count_type = count_type ))
            else:
                print("Usage: wc <filename>")
        elif command == "mkdir":
            if args:
                mkdir(args[0])
            else:
                print("Error: 'mkdir' requires a directory name.")
        elif command == "touch":
            if args:
                touch(args[0])
            else:
                print("Error: 'touch' requires a file name.")
        elif command == "cp":
            if len(args) >= 2:
                cp(args[0], args[1])
            else:
                print("Usage: cp <source> <destination>")
        elif command == "mv":
            if len(args) >= 2:
                mv(args[0], args[1])
            else:
                print("Usage: mv <source> <destination>")
        elif command == "cd":
            if args:
                result = cd(args[0])
                if result:
                    update_shell_config(result)
            else:
                result = cd(None)
                if result:
                    update_shell_config(result)
        elif command == "whoami":
            print(current_user)
        elif command == "pwd":
            pwd()
        elif command == "head":
            if len(args) >= 1:  # Command has arguments
                lines = 10  # Default number of lines
                if args[0].startswith("-") and args[0][1:].isdigit():
                    lines = int(args[0][1:])
                    args = args[1:]  # Remove the `-N` argument from args
        
                if len(args) == 1:  # File name provided
                    print(head(file_name=args[0], lines=lines))
                else:
                    print("Usage: head -<lines> <filename>")
            else:
                print("Usage: head -<lines> <filename>")

        elif command == "tail":
            if len(args) >= 1:  # Command has arguments
                lines = 10  # Default number of lines
                if args[0].startswith("-") and args[0][1:].isdigit():
                    lines = int(args[0][1:])
                    args = args[1:]  # Remove the `-N` argument from args
                    
                if len(args) == 1:  # File name provided
                    print(tail(file_name=args[0], lines=lines))
                else:
                    print("Usage: tail -<lines> <filename>")
            else:
                print("Usage: tail -<lines> <filename>")
        elif command == "echo":
            echo(args)
        elif command == "cat":
            if len(args) == 1:
                print(cat_read(args[0]))
            elif len(args) == 2 and args[0] == ">":
                cat_write(args[1], append=False)
            elif len(args) == 2 and args[0] == ">>":
                cat_write(args[1], append=True)
            else:
                print("Error: Invalid syntax for 'cat'. Use 'cat filename', 'cat > filename', or 'cat >> filename'.")
        elif command == "history":
            history()
        elif command == "rm":
            if args:
                recursive = "-r" in args
                target = args[1] if recursive else args[0]
                rm(target, recursive)
            else:
                print("Error: 'rm' requires a target file or directory.")
        elif command == "rmdir":
            if len(args) > 0:
                rmdir(args[0])
            else:
                print("Error: 'rmdir' requires a directory name.")
        elif command == "man":
            print(man(args[0]))
        elif command == "less":
            print(less(args[0]))
        elif command == "more":
            print(more(args[0]))
        elif command == "chmod":
            if len(args) >= 2:
                chmod(args[0], args[1])
            else:
                print("Usage: chmod <permissions> <name>")
        else:
            print(f"{command} not found")

    except Exception as e:
        print(f"Error executing command: {e}")

    return False  # Continue shell loop

def run_shell():
    """Main loop for running the shell."""
    while True:  # Loop to restart the shell when needed
        initialize_shell()  # Reset the shell state
        global history_index
        cmd = ""  # Initialize empty command string
        print_cmd(cmd)  # Print initial prompt

        while True:
            char = getch()  # Capture input character

            if char == "\x03":  # Ctrl-C to exit
                sys.exit(0)
            elif char == "\x7f":  # Backspace
                cmd = cmd[:-1]
                print_cmd(cmd)
            elif char == "\r":  # Enter key pressed
                print()  # Move to new line for command output
                if parse_and_execute(cmd):
                    break  # Restart the shell on specific commands like user login
                cmd = ""  # Reset command after execution
                history_index = len(command_history)
                print_cmd(cmd)  # Print new prompt for the next command
            elif char == "\x1b":  # Detect special keys (arrow keys)
                char = getch()  # Consume the next '[' character
                if char == "[":
                    char = getch()
                    if char == "A":  # Up arrow key
                        if history_index > 0:
                            history_index -= 1
                            cmd = command_history[history_index]
                            print_cmd(cmd)
                    elif char == "B":  # Down arrow key
                        if history_index < len(command_history) - 1:
                            history_index += 1
                            cmd = command_history[history_index]
                            print_cmd(cmd)
                        else:
                            history_index = len(command_history)
                            cmd = ""
                            print_cmd(cmd)
            else:
                cmd += char
                print_cmd(cmd)

if __name__ == "__main__":
    run_shell()
