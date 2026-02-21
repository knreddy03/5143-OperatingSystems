# import requests
# import os, sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# from config.config import load_config

# API_URL = "http://127.0.0.1:8080"  # Base URL of your FastAPI server

# def grep(pattern, file_name):
#     """
#     Search for a pattern in a file's content.
    
#     Args:
#         pattern (str): Pattern to search for.
#         file_name (str): Name of the file to search in.
#     """
#     config = load_config()
#     user_id = config["Settings"]["current_user_id"]
#     file_path = f"{config['Settings']['current_directory']}/{file_name}"
    
#     try:
#         response = requests.get(
#             f"{API_URL}/grep",
#             params={"file_path": file_path, "user_id": user_id, "pattern": pattern}
#         )
#         if response.status_code == 200:
#             matches = response.json().get("matches", [])
#             if matches:
#                 for line in matches:
#                     print(line)
#             else:
#                 print(f"No matches found for '{pattern}'.")
#         else:
#             print(f"Error: {response.json().get('detail', 'Unable to search file.')}")
    
#     except Exception as e:
#         print(f"Error: {e}")


from rich.console import Console
from rich.text import Text
import requests
import os, re, sys

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config

API_URL = "http://127.0.0.1:8080"  # Base URL for your API

console = Console()

import re

def grep(pattern, file_name=None, flags=None, input_data=None):
    """
    Searches for a pattern in the given input or file, highlighting matches in red.

    Args:
        pattern (str): The regex pattern to search for.
        file_name (str, optional): The name of the file to search.
        flags (list, optional): Additional flags for case insensitivity or word matching.
        input_data (str, optional): Input data from a pipeline.

    Returns:
        str: Matched lines with highlights as a single string separated by newlines.
    """
    config = load_config()
    user_id = config["Settings"]["current_user_id"]

    # Parse flags
    ignore_case = '-i' in flags if flags else False
    word_match = '-w' in flags if flags else False
    regex_flags = re.IGNORECASE if ignore_case else 0
    regex_pattern = f"\\b{pattern}\\b" if word_match else pattern  # Match full words if -w

    # ANSI escape codes for red color
    red_start = "\033[91m"
    reset_color = "\033[0m"

    matched_lines = []

    if input_data is not None:
        # Process piped input
        for line in input_data.splitlines():  # Split into individual lines
            if re.search(regex_pattern, line, regex_flags):  # Check if pattern matches
                highlighted_line = re.sub(
                    regex_pattern, 
                    lambda match: f"{red_start}{match.group(0)}{reset_color}", 
                    line, 
                    flags=regex_flags
                )
                matched_lines.append(highlighted_line)  # Add highlighted line to results
        return "\n".join(matched_lines)  # Return results as a single string

    if file_name:
        # Read and process file content
        file_path = f"{config['Settings']['current_directory']}/{file_name}"
        try:
            response = requests.get(
                f"{API_URL}/grep",
                params={"file_path": file_path, "user_id": user_id, "pattern": pattern, "ignore_case": ignore_case}
            )
            if response.status_code == 200:
                matches = response.json().get("matches", [])
                highlighted_matches = [
                    re.sub(
                        regex_pattern,
                        lambda match: f"{red_start}{match.group(0)}{reset_color}",
                        line,
                        flags=regex_flags
                    )
                    for line in matches
                ]
                return "\n".join(highlighted_matches)
            else:
                return f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}"
        except requests.RequestException as e:
            return f"Request failed: {e}"

    return "Error: No input or file specified."
