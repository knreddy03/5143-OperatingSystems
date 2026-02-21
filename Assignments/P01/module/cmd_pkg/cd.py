import requests
import os
import sys

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config, save_config

API_URL = "http://127.0.0.1:8080"  # Base URL for your API

def get_config():
    # Load configuration values from the .config file
    config = load_config()
    return (
        config["Settings"]["current_directory_id"],
        config["Settings"]["current_directory"],
        config["Settings"]["parent_id"],
        config["Settings"]["current_user_id"],
        config["Settings"]["current_user"],
    )

def save_directory_state(current_directory_id, current_directory, parent_id):
    """Helper function to save the updated directory state."""
    config = load_config()
    config["Settings"]["current_directory_id"] = current_directory_id
    config["Settings"]["current_directory"] = current_directory
    config["Settings"]["parent_id"] = parent_id
    save_config(config)

def cd(path=None):
    """
    Changes the directory based on the specified path.
    Supports root ("/"), parent (".."), named directories, and home directory (no argument).
    """
    current_directory_id, current_directory, parent_id, user_id, current_user = get_config()

    # If no path is provided, navigate to the user's home directory
    if path is None or path == "~":
        home_path = f"/home/{current_user}"
        response = requests.get(f"{API_URL}/path", params={"path": home_path, "user_id": user_id})
        if response.status_code == 200:
            home_info = response.json().get("directories", [])
            if home_info:
                home_directory = home_info[0]
                save_directory_state(home_directory["dir_id"], home_path, home_directory["parent_id"])
            else:
                print("Home directory not found.")
        else:
            print(f"Error accessing home directory: {response.text}")
        return

    # Case 1: Navigate to root (`cd /`)
    if path == "/":
        response = requests.get(f"{API_URL}/cd", params={"directory_id": 1, "user_id": user_id})
        if response.status_code == 200:
            save_directory_state(1, "/", None)
        else:
            print(f"Error accessing root directory: {response.text}")
        return

    # Case 2: Move up one level (`cd ..`)
    if path == "..":
        response = requests.get(f"{API_URL}/parent", params={"parent_id": parent_id, "user_id": user_id})
        if response.status_code == 200:
            parent_info = response.json()
            if parent_info:
                new_dir_id = parent_info["dir_id"]
                new_parent_id = parent_info["parent_id"]
                new_path = "/".join(current_directory.rstrip("/").split("/")[:-1]) or "/"
                save_directory_state(new_dir_id, new_path, new_parent_id)
            else:
                print("Already at the root directory.")
        else:
            print(f"Error moving to parent directory: {response.text}")
        return

    # Case 3: Navigate to a named subdirectory (e.g., `cd <subdir>`)
    try:
        response = requests.get(f"{API_URL}/cd", params={"directory_id": current_directory_id, "user_id": user_id})
        if response.status_code == 200:
            data = response.json()
            found = False
            for directory in data.get('subdirectories', []):
                if path == directory['name']:
                    # Update directory information
                    save_directory_state(directory["dir_id"], f"{current_directory}/{path}".replace("//", "/"), directory["parent_id"])
                    found = True
                    break

            if not found:
                print(f"No such directory: {path}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        print(f"API call failed: {e}")
