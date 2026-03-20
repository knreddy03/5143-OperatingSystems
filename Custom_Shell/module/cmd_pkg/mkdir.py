import requests, os, sys
# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config, save_config

def mkdir(directory_name):
    """
    Create a new directory in the current path.
    """
    try:

        config = load_config()
        user_id = config["Settings"]["current_user_id"]
        parent_dir = config["Settings"]["current_directory_id"]
        current_directory = config["Settings"]["current_directory"]
        path = f"{current_directory}/{directory_name}"
        # Create a new directory via FastAPI
        response = requests.post(f"http://127.0.0.1:8080/mkdir", params={"name": directory_name, "parent_id": parent_dir, "user_id": user_id, "path": path})

        if response.status_code != 200:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
