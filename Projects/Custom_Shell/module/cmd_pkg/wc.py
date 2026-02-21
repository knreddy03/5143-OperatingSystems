import requests
import os
import sys

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config

API_URL = "http://127.0.0.1:8080"  # Base URL for your API

def wc(file_name=None, piped_input=None, count_type='lines'):
    """
    Count lines, words, or characters in a file or piped input.
    
    Args:
        file_name (str, optional): Name of the file to process.
        piped_input (str, optional): Input from a pipe.
        count_type (str): What to count ('lines', 'words', or 'chars').
    Returns:
        str: The count as a string.
    """
    if file_name and not piped_input:
        # File-based input: Make an API request to count content
        config = load_config()
        user_id = config["Settings"]["current_user_id"]
        file_path = f"{config['Settings']['current_directory']}/{file_name}"

        try:
            response = requests.get(
                f"{API_URL}/wc", 
                params={"file_path": file_path, "user_id": user_id, "count_type": count_type}
            )
            if response.status_code == 200:
                return str(response.json()["count"])  # Return the count
            else:
                return f"Error: {response.json().get('detail', 'Unable to count.')}"
        except requests.RequestException as e:
            return f"Request failed: {e}"

    elif piped_input:
        # Piped input: Process the input directly
        if count_type == 'lines':
            return str(len(piped_input.splitlines()))
        elif count_type == 'words':
            return str(len(piped_input.split()))
        elif count_type == 'chars':
            return str(len(piped_input))
        else:
            return "Error: Unsupported count type."

    else:
        return "Error: Either `file_name` or `piped_input` must be provided."
