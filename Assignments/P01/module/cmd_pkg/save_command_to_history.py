import requests
import os
import sys

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config, save_config

API_URL = "http://127.0.0.1:8080"  # Base URL for your FastAPI server


def save_command_to_history(command):
    """
    saves a command to the history API.
    
    Args:
        command (str): The command to save.
    """
    config = load_config()
    user_id = config["Settings"]["current_user_id"]

    try:
        response = requests.post(f"{API_URL}/history",params={"user_id": user_id, "command": command})
        if response.status_code != 200:
            print("Warning: Could not save command to history.")
    
    except Exception as e:
        print(f"Error saving command to history: {e}")
