# Configuration Module

## Overview

The `config` module manages runtime configuration and session state for the custom shell application.

It is responsible for:

- Loading configuration from a persistent file
- Providing default configuration when necessary
- Saving runtime updates
- Centralizing system-wide settings

The configuration is stored in a JSON file named `.config` located inside the `config/` directory.

---

## Directory Structure

```
config/
│
├── .config          # Persistent configuration file
├── config.py        # Configuration management logic
└── README.md        # Module documentation
```

---

## Configuration File: `.config`

The `.config` file stores runtime state and system defaults.

### Example Configuration

```json
{
    "Settings": {
        "current_directory_id": 3,
        "current_directory": "/home/user_name",
        "current_user": "user_name",
        "current_user_id": 2,
        "parent_id": 2,
        "user_id": null
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
```

---

## Configuration Sections

### 1. Settings

Stores runtime session state:

- `current_directory_id` – ID of the current directory (database reference)
- `current_directory` – Absolute path of the current directory
- `current_user` – Active username
- `current_user_id` – Database ID of active user
- `parent_id` – Parent directory ID
- `user_id` – Used for session-related operations

This allows the shell to resume the previous state across executions.

---

### 2. Permissions

Defines default permission values:

- `default_file_permissions` – Default permission for new files (e.g., 644)
- `default_directory_permissions` – Default permission for new directories (e.g., 755)

These values are applied when creating new filesystem entities.

---

### 3. Files

- `chunk_size` – Defines the number of bytes processed at a time during file read/write operations.

Useful for handling large files efficiently.

---

### 4. Database

- `db_path` – Relative path to the SQLite database file.

Separates database configuration from business logic.

---

## config.py

The `config.py` file provides utility functions for loading and saving configuration data.

### load_config()

- Loads configuration from `.config`
- Returns default configuration if:
  - File does not exist
  - JSON decoding fails
- Prevents application crashes due to malformed config

### save_config(data)

- Saves updated configuration back to `.config`
- Formats JSON with indentation for readability
- Handles I/O errors safely

---

## Execution Flow

1. Application starts
2. `load_config()` is called
3. Configuration is loaded into memory
4. Modules use the returned configuration object
5. When state changes, `save_config()` updates the file

---

## Design Principles

- Centralized configuration management
- Safe fallback mechanism
- Separation of concerns
- No direct file manipulation outside this module
- Absolute path resolution to prevent path issues

---

## Future Improvements

- Add schema validation
- Replace print statements with structured logging
- Support environment variable overrides
- Add config versioning
- Implement concurrency safeguards
