import sys

class Getch:
    """Gets a single character from standard input. Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


def execute_command(cmd):
    """
    A placeholder function to simulate command execution.
    You can extend this to handle real shell commands.
    """
    if cmd.strip() == "pwd":
        print("/home/user")  # Simulating 'pwd' output
    elif cmd.strip() == "ls":
        print("file1.txt file2.txt dir1")  # Simulating 'ls' output
    else:
        print(f"{cmd}: command not found")  # Default message for unknown commands


if __name__ == '__main__':

    getch = Getch()  # create instance of Getch class
    prompt = "$ "  # set default prompt

    cmd = ''
    while True:  # loop forever
        char = getch()

        if char == '~':
            sys.exit(0)

        # Handle backspace
        elif char == '\x7f':  # '\x7f' is the ASCII code for backspace
            cmd = cmd[:-1]  # Remove the last character from cmd
            sys.stdout.write('\r' + ' ' * (len(prompt) + len(cmd) + 1))  # Clear line
            sys.stdout.write('\r' + prompt + cmd)  # Reprint prompt and updated cmd
            sys.stdout.flush()

        # Handle Enter key
        elif char == '\r':  # Enter key pressed
            sys.stdout.write('\n')  # Move to a new line

            if cmd.strip():  # Only process non-empty commands
                print(f"$ {cmd}")  # Display the command as in a real shell
                execute_command(cmd)  # Simulate command execution

            cmd = ''  # Reset command after execution
            sys.stdout.write(prompt)  # Print new prompt
            sys.stdout.flush()

        else:
            cmd += char
            sys.stdout.write('\r' + ' ' * (len(prompt) + len(cmd)))  # Clear line
            sys.stdout.write('\r' + prompt + cmd)  # Reprint prompt and updated cmd
            sys.stdout.flush()
