import requests
import os
import sys

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config

API_URL = "http://127.0.0.1:8080"  # Base URL for your FastAPI server


def less(file_name=None, piped_input=None):
    """
    Simulates the `less` shell command.

    Args:
        file_name (str, optional): The name of the file to paginate.
        piped_input (str, optional): Input from a piped command.
    """
    config = load_config()
    user_id = config["Settings"]["current_user_id"]
    current_path = config["Settings"]["current_directory"]
    path = f"{current_path}/{file_name}"

    lines_per_page = 10  # Default lines per page

    # For piped input, paginate the content locally
    if piped_input:
        all_lines = piped_input.splitlines()
        total_lines = len(all_lines)
        total_pages = (total_lines + lines_per_page - 1) // lines_per_page

        current_page = 1
        while True:
            start_index = (current_page - 1) * lines_per_page
            end_index = start_index + lines_per_page
            page_content = all_lines[start_index:end_index]

            print("\n".join(page_content))
            print(f"Page {current_page}/{total_pages}")
            
            user_input = input("Press Enter for next page or 'q' to quit: ").strip().lower()
            if user_input == 'q':
                break

            if current_page < total_pages:
                current_page += 1
            else:
                print("End of content.")
                break
        return

    # For file input, fetch pages from the API
    if path:
        current_page = 1

        while True:
            try:
                response = requests.get(
                    f"{API_URL}/less",
                    params={"file_path": path, "user_id": user_id, "next_page": current_page}
                )

                if response.status_code == 200:
                    data = response.json()
                    print("\n".join(data["content"]))
                    print(f"Page {data['current_page']}/{data['total_pages']}")
                    
                    if data["current_page"] == data["total_pages"]:
                        print("End of content.")
                        break

                    user_input = input("Press Enter for next page or 'q' to quit: ").strip().lower()
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
