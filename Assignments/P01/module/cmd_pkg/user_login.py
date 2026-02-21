# commands/user_login.py
import os, sys
import requests
from getpass import getpass
# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config, save_config

def clear_screen():
    """Clears the terminal screen."""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def user_login(username: str):
    """
    Logs in a user by interacting with the FastAPI backend.
    Prompts for the password with up to 3 chances if the password is incorrect.
    
    :param username: The username provided with the command (su username or sudo username)
    """
        
    # Attempt login up to 3 times for incorrect passwords
    max_attempts = 3
    
    for attempt in range(max_attempts):
        # Securely get the password without echo
        password = getpass(f"Password for {username}: ")
        
        
        try:
            # Send a POST request to the FastAPI login route
            response = requests.post(f"http://127.0.0.1:8080/user_login", params={"username": username, "password": password})
            
            # Check if the login was successful
            if response.status_code == 200:
                clear_screen()  
                print(f"Welcome, {username}!")
                
                # Restart the shell after successful login
                os.system("python3 shell.py")
                sys.exit(0)  # Exit the current shell process to avoid duplicate shells

            elif response.status_code == 400:
                if attempt < max_attempts - 1:
                    print("Sorry, try again.")
                else:
                    print("Maximum attempts reached. Login failed.")
                    return  # Do not update values, exit after 3 failed attempts
                
            elif response.status_code == 404:
                print(f"Error: User '{username}' not found.")
                return  # Exit if user is not found
            
            else:
                print(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
                return  # Exit on other errors
        
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to connect to the server. {e}")
            return  # Exit on connection error

