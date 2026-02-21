import requests
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config

API_URL = "http://127.0.0.1:8080"  # Base URL of your FastAPI server

def tail(file_name=None, lines=10, piped_input=None):
    """
    Fetch the last `n` lines of a file or process piped input.
    
    Args:
        file_name (str, optional): Name of the file.
        lines (int, optional): Number of lines to fetch from the end. Default is 10.
        piped_input (str, optional): Input data from another command.
    
    Returns:
        str: The last `n` lines of the file or piped input.
    """
    if piped_input:
        # Handle piped input directly
        input_lines = piped_input.splitlines()
        if len(input_lines) >= lines:
            return "\n".join(input_lines[-lines:])
        return "\n".join(input_lines)  # Return all lines if fewer than requested
    
    if file_name:
        # Handle file input via API
        config = load_config()
        user_id = config["Settings"].get("current_user_id")
        file_path = f"{config['Settings']['current_directory']}/{file_name}"
        
        try:
            response = requests.get(
                f"{API_URL}/tail", 
                params={"file_path": file_path, "user_id": user_id, "lines": lines}
            )
            if response.status_code == 200:
                return response.json().get("content", "")
            else:
                return f"Error: {response.json().get('detail', 'Unable to fetch file content.')}"
        except requests.RequestException as e:
            return f"Request failed: {e}"

    return "Error: Either `file_name` or `piped_input` must be provided."
