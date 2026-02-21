import requests
import os
import sys

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config, save_config

API_URL = "http://127.0.0.1:8080"  # Base URL for your FastAPI server

def cat_read(file_name=None, piped_input=None):
    """
    Reads and displays the content of a file or piped input.
    
    Args:
        file_name (str, optional): Name of the file to read.
        piped_input (str, optional): Input from a previous command in the pipeline.
    """
    if piped_input:
        # Handle piped input
        return piped_input

    if file_name:
        # Call the API to fetch file content
        config = load_config()
        user_id = config["Settings"]["current_user_id"]
        file_path = f"{config['Settings']['current_directory']}/{file_name}"

        try:
            response = requests.get(f"{API_URL}/cat", params={"file_path": file_path, "user_id": user_id})
            if response.status_code == 200:
                lines = response.json()
                return "\n".join(lines["lines"])  # Return the lines joined with newline characters
            else:
                return f"Error: {response.json().get('detail', 'Unable to read file.')}"
        except requests.RequestException as e:
            return f"Request failed: {e}"

    return "Error: No file name or piped input provided."
