import requests, os, sys
# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config, save_config

def touch(file_name):
    """
    Create a new file in the current directory.
    """
    try:
        config = load_config()
        user_id = config["Settings"]["current_user_id"]
        parent_id = config["Settings"]["current_directory_id"]
        current_directory = config["Settings"]["current_directory"]
        path = f"{current_directory}/{file_name}"

        response = requests.post(f"http://127.0.0.1:8080/touch", params={"name": file_name, "parent_id": parent_id, "user_id": user_id, "path": path})

        if response.status_code != 200:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

