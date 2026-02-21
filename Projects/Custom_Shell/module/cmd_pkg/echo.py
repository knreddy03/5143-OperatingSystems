# echo.py

def echo(args):
    """
    Simulates the echo command with optional flags.
    
    Args:
        args (list): Arguments passed to echo command.
    """
    # Remove surrounding quotes from each argument if present
    output = " ".join(arg.strip('"') for arg in args)

    # Check if '-n' is the first argument to suppress newline
    if len(args) > 0 and args[0] == "-n":
        output = " ".join(arg.strip('"') for arg in args[1:])
        print(output, end="")  # Suppress newline at the end
    else:
        print(output)  # Print with newline
