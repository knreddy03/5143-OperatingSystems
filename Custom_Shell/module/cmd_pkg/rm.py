import requests
import os
import sys

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config, save_config
from cmd_pkg import cd

API_URL = "http://127.0.0.1:8080"  # Base URL for your FastAPI server

def rm(name, recursive=False):
    """
    Deletes a file or directory from the virtual file system.

    Args:
        name (str): The name of the file or directory to delete.
        recursive (bool): If True, delete directories and contents recursively.
    """
    # Load config and determine current path
    config = load_config()
    current_user_id = config["Settings"]["current_user_id"]
    current_directory = config["Settings"]["current_directory"]
    if current_directory.split("/")[-1] == name:
        path = current_directory
    else:
        path = f"{current_directory}/{name}"

    # Perform the deletion request
    try:
        response = requests.delete(
            f"{API_URL}/rm",
            params={"path": path, "user_id": current_user_id, "recursive": recursive}
        )
        if response.status_code == 200:
            # If recursive, update config to reflect parent directory
            if recursive and path == current_directory:
                cd("..")
                # update_config_to_parent_directory()
        else:
            error_message = response.json().get("detail", "Unknown error occurred.")
            print(f"Error deleting '{name}': {error_message}")
    except Exception as e:
        print(f"Error: {e}")


def update_config_to_parent_directory():
    """
    Updates the configuration to the parent directory after recursive deletion.
    """
    config = load_config()
    user_id = config["Settings"]["current_user_id"]
    parent_id = config["Settings"]["parent_id"]

    try:
        response = requests.get(f"{API_URL}/parent", params={"parent_id": parent_id, "user_id": user_id})
        if response.status_code == 200:
            parent_info = response.json()
            # Update config values if parent directory exists
            if parent_info:
                config["Settings"]["parent_id"] = parent_info.get("parent_id", None)
                config["Settings"]["current_directory_id"] = parent_info.get("dir_id", None)
                config["Settings"]["current_directory"] = "/".join(
                    config["Settings"]["current_directory"].rstrip("/").split("/")[:-1]
                ) or "/"
                save_config(config)
        else:
            print(f"Error retrieving parent directory: {response.json().get('detail', 'Unknown error.')}")
    except Exception as e:
        print(f"Error updating configuration: {e}")
