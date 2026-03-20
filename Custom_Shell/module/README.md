# Module Package – Shell Core Architecture

## Overview

The `module` package represents the core runtime layer of the custom database-backed shell.

It contains:

- Shell runtime engine
- Configuration management
- Terminal input handling
- Permission modeling
- Database abstraction layer
- Command implementation subpackage (`cmd_pkg`)

This package forms the backbone of the entire system.

---

## High-Level Architecture

```
User Input
    ↓
getch.py (Terminal Input Handler)
    ↓
shell.py (Runtime Engine)
    ↓
Command Dispatcher
    ↓
cmd_pkg/ (Command Implementations)
    ↓
sqliteCRUD.py (Database Layer)
    ↓
SQLite Database
```

The `module` package orchestrates interaction between user input, command execution, and persistent storage.

---

## Package Structure

```
module/
│
├── config.py
├── getch.py
├── permissions.py
├── shell.py
├── sqliteCRUD.py
│
└── cmd_pkg/
      ├── File & Directory Commands
      ├── Content Commands
      ├── User Management Commands
      ├── History Commands
      └── README.md
```

---

# Core Infrastructure Files

---

## 1. `config.py`

Manages runtime configuration and session persistence.

Responsibilities:

- Load `.config` file
- Provide default fallback configuration
- Persist state updates
- Store:
  - Current directory
  - Current user
  - Database path
  - Default permissions
  - File chunk size

Key Functions:

- `load_config()`
- `save_config(data)`

This enables persistent state across shell restarts.

---

## 2. `getch.py`

Implements low-level terminal input handling.

Features:

- Character-by-character input
- Arrow key detection
- Backspace handling
- Ctrl+C handling
- Cross-platform support (Unix / Windows)
- Interactive prompt rendering

This allows the shell to behave like a real Unix terminal instead of using basic `input()`.

---

## 3. `permissions.py`

Implements Unix-style permission modeling.

Functions:

- `convert_permission(triple)`
- `convert_digit(digit)`

Example:

```python
convert_permission(755)
# Output: "rwxr-xr-x"
```

Supports:

- Owner permissions
- Group permissions
- Others permissions

Used by command implementations to enforce access control.

---

## 4. `sqliteCRUD.py`

Database abstraction layer.

Class: `SqliteCRUD`

Purpose:

- Encapsulate SQLite operations
- Provide structured CRUD interface
- Standardize response format
- Isolate SQL from command logic

### Response Format

All database operations return:

```python
{
    "query": "...",
    "success": True/False,
    "message": "...",
    "affected": int,
    "data": list
}
```

This ensures consistent communication between infrastructure and commands.

---

## 5. `shell.py`

Core runtime engine of the system.

Responsibilities:

- Initialize shell state
- Load configuration
- Manage command history
- Handle login switching (`su`, `sudo`)
- Parse commands
- Execute pipelines (`|`)
- Dispatch commands to `cmd_pkg`
- Restart shell session when needed

---

### Key Runtime Functions

#### `initialize_shell()`

- Loads configuration
- Sets current directory
- Loads user history
- Prepares runtime context

---

#### `parse_and_execute(cmd)`

Main dispatcher function.

- Parses user input
- Identifies command
- Routes execution to corresponding module in `cmd_pkg`
- Handles invalid commands
- Manages built-in runtime behaviors

---

#### `execute_pipeline(cmd)`

Implements pipe (`|`) behavior.

Example:

```
cat file.txt | grep hello | wc -l
```

Flow:

1. Split by `|`
2. Execute first command
3. Pass output to next command
4. Continue chaining
5. Print final result

Implements in-memory data streaming between commands.

---

#### `run_shell()`

Main interactive loop.

Handles:

- Continuous input reading
- Arrow-key history navigation
- Backspace editing
- Ctrl+C interruption
- Prompt rendering
- Session restart logic

This simulates a real interactive shell environment.

---

# Command Subpackage: `cmd_pkg`

The `cmd_pkg` directory is a subpackage inside `module`.

It contains individual command implementations, such as:

- `ls.py`
- `mkdir.py`
- `touch.py`
- `cp.py`
- `mv.py`
- `cat_read.py`
- `grep.py`
- `wc.py`
- `chmod.py`
- `user_login.py`
- and more

Each file represents a single command and follows the Single Responsibility Principle.

The shell runtime dynamically dispatches commands to this subpackage.

See `cmd_pkg/README.md` for detailed command documentation.

---

# Design Principles

- Layered architecture
- Clear separation between runtime and commands
- Database-backed virtual filesystem
- Unix-style permission enforcement
- Persistent session configuration
- Modular and extensible design
- Pipeline execution support
- Multi-user system modeling

---

# Engineering Significance

The `module` package implements:

- A mini Unix-like shell runtime
- Database-backed virtual filesystem
- Permission system
- Pipeline execution engine
- Interactive terminal handler
- Multi-user environment

It serves as the system core that powers all command execution.

This is not a basic CLI script — it is a layered shell architecture with persistence, access control, and modular extensibility.

---

# Future Improvements

- Dynamic command auto-discovery using `importlib`
- Plugin-based command loading
- Structured logging layer
- Secure password hashing
- Role-based access control
- Thread-safe database handling
- Improved error handling hierarchy
- Automated testing framework

