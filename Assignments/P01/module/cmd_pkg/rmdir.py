import sys
import os
import requests

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config

API_URL = "http://127.0.0.1:8080"  # Base URL for your FastAPI server

def rmdir(name):
    """
    Deletes an empty directory from the virtual file system.
    
    Args:
        name (str): The name of the directory to delete.
    """
    # Load configuration values
    config = load_config()
    current_user_id = config["Settings"]["current_user_id"]
    current_directory = config["Settings"]["current_directory"]
    path = f"{current_directory}/{name}"

    try:
        # Send DELETE request to the /rmdir endpoint
        response = requests.delete(
            f"{API_URL}/rmdir",
            params={"path": path, "user_id": current_user_id}
        )

        # Handle successful deletion or error messages
        if response.status_code != 200:
            error_message = response.json().get("detail", "Unknown error occurred.")
            print(f"Error deleting directory '{name}': {error_message}")
    except Exception as e:
        print(f"Error: {e}")
