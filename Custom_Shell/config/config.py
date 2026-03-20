import json
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the absolute path for the .config file
config_path = os.path.join(script_dir, ".config")  # This makes the path absolute

# Default configuration template (optional)
default_config = {
    "Settings": {
        "current_directory_id": None,
        "current_directory": "/home",
        "current_user": "guest",
        "current_user_id": None,
        "parent_id": None
    },
    "Permissions": {
        "default_file_permissions": 644,
        "default_directory_permissions": 755
    },
    "Files": {
        "chunk_size": 1024
    },
    "Database": {
        "db_path": "./data/filesystem.db"
    }
}

def load_config():
    """Load configuration from .config file, or return default config if not found."""
    if not os.path.exists(config_path):
        print("Config file not found. Using default configuration.")
        return default_config.copy()  # Return a copy to avoid modifying the default template

    with open(config_path, 'r') as config_file:
        try:
            config = json.load(config_file)
            # print("Configuration loaded successfully.")
            return config
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return default_config.copy()  # Return default config on error

def save_config(data):
    """Save the configuration data back to the .config file."""
    try:
        with open(config_path, 'w') as config_file:
            json.dump(data, config_file, indent=4)  # Pretty print the JSON
            # print("Configuration saved successfully.")
    except IOError as e:
        print(f"Error saving configuration: {e}")

