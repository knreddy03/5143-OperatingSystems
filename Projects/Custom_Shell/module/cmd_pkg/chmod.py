import requests
import os
import sys

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config

API_URL = "http://127.0.0.1:8080"  # Base URL of your FastAPI server

def chmod(permissions, name):
    """
    Changes file permissions.

    Args:
        permissions (str): Permissions in either numeric (e.g., "755") or symbolic format (e.g., "+x", "u+w").
        name (str): The file to change permissions for.
    """
    config = load_config()
    user_id = config["Settings"]["current_user_id"]
    file_path = f"{config['Settings']['current_directory']}/{name}"

    try:
        # Send POST request to chmod API route
        response = requests.post(
            f"{API_URL}/chmod",
            params={"file_path": file_path, "user_id": user_id, "permissions": permissions}
        )

        # Check the response status
        if response.status_code != 200:
            print(f"Error: {response.json().get('detail', 'Unable to change permissions.')}")
    
    except requests.RequestException as e:
        print(f"Error: {e}")
