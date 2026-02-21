import requests
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config

API_URL = "http://127.0.0.1:8080"  # Base URL of your FastAPI server


def cp(source, destination):
    """
    Copies a file or directory from source to destination.

    Args:
        source (str): Source path of the file or directory.
        destination (str): Destination path for the copied file or directory.
    """
    config = load_config()
    user_id = config["Settings"]["current_user_id"]
    current_directory = config["Settings"]["current_directory"]

    # Determine absolute paths
    source_path = f"{current_directory}/{source}".rstrip('/')
    destination_path = f"{current_directory}/{destination}".rstrip('/')

    try:
        response = requests.post(
            f"{API_URL}/cp",
            params={"source_path": source_path, "destination_path": destination_path, "user_id": user_id}
        )
        if response.status_code != 200:
            print(f"Error: {response.json().get('detail', 'Unable to copy item.')}")
    except requests.RequestException as e:
        print(f"Error: Failed to make request: {e}")
    except Exception as e:
        print(f"Error: {e}")
