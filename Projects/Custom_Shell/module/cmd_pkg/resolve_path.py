import requests

API_URL = "http://127.0.0.1:8000"  # Base URL for your FastAPI server

def resolve_path(path, user_id=1):
    """
    Resolves a given path to get the corresponding directory or file ID.
    
    Args:
        path (str): The path to resolve.
        user_id (int): The ID of the user (default: 1).
    
    Returns:
        int: The resolved directory or file ID.
    """
    url = f"{API_URL}/resolve"
    try:
        response = requests.get(url, params={"path": path, "user_id": user_id})
        if response.status_code == 200:
            data = response.json()
            return data['id']  # Return the resolved directory/file ID
        else:
            print(f"Error resolving path: {response.json()['detail']}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
