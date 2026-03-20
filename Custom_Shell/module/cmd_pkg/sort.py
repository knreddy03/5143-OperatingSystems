import requests
import os
import sys, re

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config

API_URL = "http://127.0.0.1:8080"  # Base URL for your FastAPI server

def sort(file_name=None, piped_input=None, flags=[]):
    """
    Implements the `sort` shell command.

    Args:
    - file_name (str, optional): File to be sorted.
    - piped_input (str, optional): Input from a piped command.
    - flags (list): Flags to modify the sort behavior.

    Returns:
    - str: Sorted output.
    """
    config = load_config()
    user_id = config["Settings"]["current_user_id"]

    # Parse flags
    numeric = "-n" in flags if flags else False
    reverse = "-r" in flags if flags else False
    case_insensitive = "-f" in flags if flags else False
    unique = "-u" in flags if flags else False

    # Handle piped input directly
    if piped_input is not None:
        content = piped_input.splitlines()
        print(content)
        if case_insensitive:
            key_func = str.lower
        elif numeric:
            key_func = lambda x: float(re.search(r"\d+", x).group()) if re.search(r"\d+", x) else float('inf')
        else:
            key_func = None

        sorted_content = sorted(content, key=key_func, reverse=reverse)

        if unique:
            sorted_content = list(dict.fromkeys(sorted_content))

        return "\n".join(sorted_content)

    # Handle file-based sorting via API
    if file_name:
        file_path = f"{config['Settings']['current_directory']}/{file_name}"

        try:
            response = requests.get(f"{API_URL}/sort", params = {
            "file_path": file_path,
            "user_id": user_id,
            "numeric": numeric,
            "reverse": reverse,
            "case_insensitive": case_insensitive,
            "unique": unique
        })
            if response.status_code == 200:
                return "\n".join(response.json().get("content", []))
            else:
                return f"Error: {response.json().get('detail', 'Unable to sort content.')}"
        except Exception as e:
            return f"Error: {e}"

    return "Error: No file or input provided for sorting."
