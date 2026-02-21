import requests

def touch(username, password):
    """
    Create a new file in the current directory.
    """
    try:

        response = requests.post(f"http://127.0.0.1:8080/adduser", params={"username": username, "password": password})

        if response.status_code == 200:
            print(f"File '{username}' created.")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

