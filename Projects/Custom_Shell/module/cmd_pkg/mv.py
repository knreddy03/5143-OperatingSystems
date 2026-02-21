import requests
import os
import sys

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config

API_URL = "http://127.0.0.1:8080"  # Base URL of your FastAPI server

def mv(source, destination):
    """
    Moves a file or directory from source to destination.

    Args:
        source (str): Source path of the file or directory.
        destination (str): Destination path for the moved file or directory.
    """
    config = load_config()
    user_id = config["Settings"]["current_user_id"]
    current_directory = config["Settings"]["current_directory"]

    # Construct absolute paths for source and destination
    source_path = f"{current_directory}/{source}".rstrip('/')
    destination_path = f"{current_directory}/{destination}".rstrip('/')

    try:
        # Send a POST request to the mv API route
        response = requests.post(
            f"{API_URL}/mv",
            params={
                "source_path": source_path,
                "destination_path": destination_path,
                "user_id": user_id
            }
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error occurred.')}")
    except requests.RequestException as e:
        print(f"Error: Unable to connect to the server: {e}")
    except Exception as e:
        print(f"Error: {e}")
