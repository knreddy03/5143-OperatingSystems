import requests
import os
import sys

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config

API_URL = "http://127.0.0.1:8080"  # Base URL for your FastAPI server


def more(file_name=None, piped_input=None):
    """
    Simulates the `more` command for displaying content one screen at a time.

    Args:
        path (str, optional): The name of the file to display.
        piped_input (str, optional): Input data from a piped command.
    """
    config = load_config()
    user_id = config["Settings"]["current_user_id"]
    current_path = config["Settings"]["current_directory"]
    path = f"{current_path}/{file_name}"

    lines_per_screen = 10  # Default lines per screen

    if piped_input:
        # Handle piped input
        all_lines = piped_input.splitlines()
        total_lines = len(all_lines)
        for start in range(0, total_lines, lines_per_screen):
            print("\n".join(all_lines[start:start + lines_per_screen]))
            user_input = input("Press Enter for next screen or 'q' to quit: ").strip().lower()
            if user_input == 'q':
                break
    elif path:
        # Handle file input via API
        current_page = 1
        while True:
            try:
                response = requests.get(
                    f"{API_URL}/more",
                    params={"file_path": path, "user_id": user_id, "next_page": current_page}
                )
                if response.status_code == 200:
                    data = response.json()
                    print("\n".join(data["content"]))
                    print(f"Screen {data['current_page']}/{data['total_pages']}")
                    if data["current_page"] == data["total_pages"]:
                        print("End of content.")
                        break

                    user_input = input("Press Enter for next screen or 'q' to quit: ").strip().lower()
                    if user_input == 'q':
                        break

                    current_page += 1
                else:
                    print(f"Error: {response.json().get('detail', 'Unable to fetch content.')}")
                    break
            except Exception as e:
                print(f"Error: {e}")
                break
    else:
        print("Error: No file name or piped input provided.")
