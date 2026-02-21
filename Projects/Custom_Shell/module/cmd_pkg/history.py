import requests
import os
import sys

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config, save_config

API_URL = "http://127.0.0.1:8080"  # Base URL for your FastAPI server


def history(piped_input=None):
    """
    Fetches and displays the command history for the current user or returns it for piping.

    Args:
        piped_input (str, optional): Input data from a previous command in a pipeline.

    Returns:
        str: Command history as a string.
    """
    config = load_config()
    user_id = config["Settings"]["current_user_id"]

    try:
        response = requests.get(f"{API_URL}/history", params={"user_id": user_id})
        if response.status_code == 200:
            history_data = response.json()["history"]
            history_output = "\n".join(f"{i + 1} {entry['command']}" for i, entry in enumerate(history_data))

            if piped_input is not None:
                # Return the history as a string for piped commands
                return history_output

            # Print history for standalone use
            print(history_output)

            # Return history list for lookup
            return [entry["command"] for entry in history_data]
        else:
            error_message = f"Error retrieving command history: {response.json().get('detail', 'Unknown error')}"
            if piped_input is not None:
                return error_message
            print(error_message)
    except Exception as e:
        error_message = f"Error: {e}"
        if piped_input is not None:
            return error_message
        print(error_message)
