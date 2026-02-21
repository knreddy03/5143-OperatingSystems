import requests
import os, sys
from rich import print
from rich.console import Console
from rich.text import Text

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config, save_config

API_URL = "http://127.0.0.1:8080"  # Base URL of your API

console = Console()

def get_config():
    """Reads configuration values from the .config file."""
    config = load_config()
    user_id = config["Settings"]["current_user_id"]
    user = config["Settings"]["current_user"]
    parent_dir = config["Settings"]["current_directory_id"]
    return user_id, parent_dir, user

def ls(flags=None):
    """
    Lists the contents of the current directory using the API, supporting flags:
    - `-a`: Show hidden files
    - `-l`: Detailed view
    - `-h`: Human-readable sizes
    
    Args:
        flags (list): List of flags (e.g., ['-a', '-l', '-h']).
    """
    user_id, parent_dir, user = get_config()

    show_hidden = '-a' in flags if flags else False
    detailed = '-l' in flags if flags else False
    human_readable = '-h' in flags if flags else False
    
    try:
        response = requests.get(
            f"{API_URL}/ls",
            params={
                "did": parent_dir,
                "user_id": user_id,
                "show_hidden": show_hidden,
                "detailed": detailed,
                "human_readable": human_readable
            }
        )
        
        if response.status_code == 200:
            contents = response.json()
            directories = contents.get("directories", [])
            files = contents.get("files", [])

            if detailed or show_hidden or human_readable:
                print(Text("Permissions Owner  Group    Size      Modified         Name", style="bold yellow"))
                print("-------------------------------------------------------------")
                total_size = contents.get("total", "")
                if total_size:
                    print("total ", Text(f"{total_size}", style="bold green"))

                # Print each directory in detailed format
                for directory in directories:
                    dir_text = Text(directory['name'], style="bold blue")
                    print(f"{directory['permissions']}   {user}    {user} "
                          f"{str(directory['size']).rjust(8)}  {directory['modified_at']}  ", end="")
                    print(dir_text, end="")
                    if show_hidden:
                        print("/")  # Adding "/" at the end to indicate it's a directory
                    else:
                        print()
                # Print each file in detailed format
                for file in files:
                    print(f"{file['permissions']}   {user}    {user} "
                                  f"{str(file['size']).rjust(8)}  {file['modified_at']}  {file['name']}")
            elif flags == []:
                # Basic view: Print directories and files in rows with up to 6 items per row
                combined = [
                    (Text(directory['name'], style="bold blue"), True) for directory in directories
                ] + [
                    (Text(file['name'], style="white"), False) for file in files
                ]

                max_columns = 6
                row = []

                for index, (item, directory) in enumerate(combined, start=1):
                    row.append(item)
                    if index % max_columns == 0 or index == len(combined):
                        print(*row, sep="  ")
                        row = []
        else:
            print(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}", style="red")
    
    except requests.RequestException as e:
        print(f"API call failed: {e}", style="red")
