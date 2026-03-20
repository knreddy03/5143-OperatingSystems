import requests
import os
import sys

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config, save_config

API_URL = "http://127.0.0.1:8080"  # Base URL for your FastAPI server

def get_user_history():
    """
    Fetches and returns the command history for the current user.
    """
    config = load_config()
    user_id = config["Settings"]["current_user_id"]

    try:
        response = requests.get(f"{API_URL}/history", params={"user_id": user_id})
        if response.status_code == 200:
            history_data = response.json()["history"]
            return {i + 1: entry["command"] for i, entry in enumerate(history_data)}
        else:
            print("Error retrieving command history:", response.json().get("detail", "Unknown error"))
            return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}

def exe_cmd_by_num(command_number):
    """
    Get a command from history based on its number.
    Args:
        command_number (int): The command number to fetch.
    Returns:
        str: The command string.
    """
    history = get_user_history()
    if command_number not in history:
        print(f"Error: No command at position {command_number} in history.")
        return None

    cmd = history[command_number]
    print(f"{cmd}")  # Display the command being fetched
    return cmd
