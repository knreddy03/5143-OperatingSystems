COMMAND_DOCS = {
    "grep": """
    grep - search for a pattern in a file or input.

    Usage:
        grep [OPTIONS] PATTERN [FILE]

    Options:
        -i    Ignore case distinctions.
        -w    Match only whole words.
        -c    Count matching lines.
    """,
    "wc": """
    wc - print newline, word, and byte counts for each file or input.

    Usage:
        wc [OPTIONS] [FILE]

    Options:
        -l    Print the number of lines.
        -w    Print the number of words.
        -c    Print the number of bytes.
    """,
    "cat": """
    cat - concatenate and display file contents.

    Usage:
        cat [FILE]

    Description:
        Concatenates and writes file contents to the standard output.
    """,
    "man": """
    man - display the manual for a command.

    Usage:
        man [COMMAND]

    Description:
        Displays detailed help for the specified command.
    """,
    "echo": """
    echo - display a line of text.

    Usage:
        echo [TEXT]

    Description:
        Writes the provided text to standard output.
    """,
    "head": """
    head - output the first part of files.

    Usage:
        head [OPTIONS] [FILE]

    Options:
        -n NUM  Print the first NUM lines of the file (default: 10).
    """,
    "tail": """
    tail - output the last part of files.

    Usage:
        tail [OPTIONS] [FILE]

    Options:
        -n NUM  Print the last NUM lines of the file (default: 10).
    """,
    "touch": """
    touch - create an empty file or update the timestamp of a file.

    Usage:
        touch [FILE]

    Description:
        Creates a new file if it doesn't exist, or updates the timestamp of an existing file.
    """,
    "rm": """
    rm - remove files or directories.

    Usage:
        rm [OPTIONS] [FILE]

    Options:
        -r    Recursively delete directories and their contents.
        -f    Force delete files without prompting.
    """,
    "mv": """
    mv - move or rename files.

    Usage:
        mv SOURCE DEST

    Description:
        Moves the file or directory from SOURCE to DEST. Can also be used to rename files.
    """,
    "cp": """
    cp - copy files and directories.

    Usage:
        cp [OPTIONS] SOURCE DEST

    Options:
        -r    Recursively copy directories and their contents.
    """,
    "chmod": """
    chmod - change file permissions.

    Usage:
        chmod MODE FILE

    Description:
        Changes the permissions of a file. MODE can be numeric (e.g., 755) or symbolic (e.g., u+x).
    """,
    "mkdir": """
    mkdir - create directories.

    Usage:
        mkdir [OPTIONS] DIRECTORY

    Options:
        -p    Create parent directories as needed.
    """,
    "history": """
    history - show previously executed commands.

    Usage:
        history

    Description:
        Displays a list of previously executed commands in the current session.
    """
}

def man(command):
    """
    Displays the manual page for the given command.

    Args:
        command (str): The name of the command.

    Returns:
        str: The documentation for the command, or an error message if the command is not found.
    """
    if command in COMMAND_DOCS:
        return COMMAND_DOCS[command]
    else:
        return f"No manual entry for '{command}'. Use 'man' to see available commands."
