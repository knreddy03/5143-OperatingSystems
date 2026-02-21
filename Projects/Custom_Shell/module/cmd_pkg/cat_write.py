import requests
import os
import sys

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config, save_config

API_URL = "http://127.0.0.1:8080"  # Base URL for your FastAPI server

def cat_write(file_name, append=False):
    """
    Collects multiline input from the user and writes/appends it to a file.
    
    Args:
        file_name (str): The name of the file to write to.
        append (bool): Whether to append to the file (True) or overwrite (False).
    """
    config = load_config()
    user_id = config["Settings"]["current_user_id"]
    current_directory = config["Settings"]["current_directory"]
    file_path = f"{current_directory}/{file_name}"

    print("Enter content to write to the file. Press Ctrl+D (or Ctrl+Z on Windows) to save and exit.")

    # Capture multiline input
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass  # End input with Ctrl+D (or Ctrl+Z on Windows)

    # Join lines and send to API
    content = "\n".join(lines)
    try:
        response = requests.post(
            f"{API_URL}/cat_write",
            params={
                "file_path": file_path,
                "user_id": user_id,
                "content": content,
                "append": append
            }
        )
        if response.status_code != 200:
            print(f"Error: {response.json().get('detail', 'Unable to write to file.')}")

    except Exception as e:
        print(f"Error: {e}")
