# Data Module

## Overview

The `data` module is responsible for initializing and managing the database schema for the custom shell filesystem.

It creates the SQLite database and defines all tables required to simulate:

- Files
- Directories
- File contents
- Users
- Command history
- Manual pages (man commands)
- Permission system

The database models a simplified Unix-like filesystem with user-level permission control.

---

## File Structure

```
data/
│
├── createdb.py     # Database schema initialization script
└── README.md       # Module documentation
```

---

## Database Overview

The system uses SQLite as its backend database.

The schema simulates a hierarchical filesystem with:

- Self-referencing directories
- File chunk storage
- Owner / Group / Others permission model
- User management
- Command history tracking

---

## Tables

### 1. files

Stores metadata for files.

Key Fields:

- `file_id` – Primary key
- `name` – File name
- `parent_id` – Directory containing the file
- `user_id` – Owner of the file
- `size` – File size in bytes
- `path` – Absolute path
- `created_at`, `modified_at` – Timestamps

Permission Fields:

- Owner: read / write / execute
- Group: read / write / execute
- Others: read / write / execute

Files reference:
- `directories(dir_id)`
- `users(user_id)`

---

### 2. directories

Stores directory metadata.

Key Fields:

- `dir_id` – Primary key
- `name` – Directory name
- `parent_id` – Self-referencing for nested directories
- `user_id` – Owner
- `path` – Absolute path

Directories follow Unix-style permission rules:

- Execute permission enabled by default
- Self-referencing foreign key allows hierarchical structure

---

### 3. file_contents

Stores file data in chunks.

Purpose:

- Enables large file storage
- Improves memory efficiency
- Allows streaming-style reads

Fields:

- `file_id` – Reference to file
- `chunk` – BLOB data
- `chunk_index` – Order of chunk

This design avoids storing large files in a single row.

---

### 4. users

Stores system users.

Fields:

- `user_id`
- `username` (unique)
- `password`
- `created_at`

Default users inserted during initialization:

- root
- bob
- mia
- raj

---

### 5. history

Tracks command history per user.

Fields:

- `history_id`
- `user_id`
- `commands`

Allows implementation of shell history features.

---

### 6. mans

Stores manual entries for commands.

Fields:

- `command_name`
- `man_command`

Supports a custom `man` command inside the shell.

---

## Permission Model

The system follows a Unix-inspired permission model:

- Owner permissions
- Group permissions
- Others permissions

Each permission consists of:

- Read
- Write
- Execute

These are stored as boolean fields in both `files` and `directories`.

---

## Execution Flow

When `createdb.py` runs:

1. Connects to SQLite database (`filesystem.db`)
2. Creates tables if they do not exist
3. Inserts default users (with conflict protection)
4. Commits changes
5. Closes connection

---

## Design Considerations

- Self-referencing directories allow nested folder structure
- Chunk-based file storage improves scalability
- Permission system enables realistic access control
- Database-driven filesystem ensures persistence
- Schema avoids duplication using foreign keys

---

## Future Improvements

- Add password hashing (currently plain text)
- Add group table for real group-based permissions
- Add indexing for performance
- Add triggers to auto-update `modified_at`
- Improve foreign key constraints for man commands table
- Add cascading deletes for cleaner directory removal
