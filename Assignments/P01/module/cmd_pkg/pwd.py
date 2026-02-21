import os, sys

# Add the parent directory to sys.path to fix the import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config.config import load_config, save_config

def pwd():
    config = load_config()

    print(config["Settings"]["current_directory"])