# cmd_pkg – Command Execution Layer

## Overview

The `cmd_pkg` directory contains all command implementations for the custom database-backed shell.

Each file inside this package represents a single command, following a modular architecture similar to real Unix shell command structures.

This design ensures:

- Separation of concerns
- Scalability
- Maintainability
- Easy addition of new commands
- Clean dispatch architecture

---

## Architecture Philosophy

Instead of placing all command logic in one file, each command is implemented as its own module.

This mirrors real-world CLI systems and improves long-term extensibility.

```
User Input
    ↓
Command Dispatcher
    ↓
cmd_pkg.<command>.py
    ↓
Database / Filesystem Layer
    ↓
SQLite Storage
```

---

## Directory Structure

```
cmd_pkg/
│
├── add_user.py
├── cat_read.py
├── cat_write.py
├── cd.py
├── chmod.py
├── cp.py
├── echo.py
├── exec_cmd_by_num.py
├── exit.py
├── grep.py
├── head.py
├── history.py
├── less.py
├── ls.py
├── man.py
├── mkdir.py
├── more.py
├── mv.py
├── pwd.py
├── resolve_path.py
├── rm.py
├── rmdir.py
├── save_command_to_history.py
├── sort.py
├── tail.py
├── touch.py
├── user_login.py
├── users.py
├── wc.py
└── README.md
```

---

## Command Categories

### File & Directory Management

| File | Purpose |
|------|----------|
| `ls.py` | List directory contents |
| `mkdir.py` | Create directory |
| `rmdir.py` | Remove directory |
| `cd.py` | Change directory |
| `pwd.py` | Print working directory |
| `touch.py` | Create empty file |
| `rm.py` | Remove file |
| `cp.py` | Copy file |
| `mv.py` | Move/Rename file |
| `resolve_path.py` | Handles absolute & relative path resolution |

---

### File Content Commands

| File | Purpose |
|------|----------|
| `cat_read.py` | Read file contents |
| `cat_write.py` | Write to file |
| `head.py` | Show first N lines |
| `tail.py` | Show last N lines |
| `less.py` | Paginated file viewer |
| `more.py` | Basic file viewer |
| `sort.py` | Sort file content |
| `wc.py` | Word/line/char count |
| `grep.py` | Pattern search inside file |
| `echo.py` | Print text / redirect content |

---

### Permissions & Security

| File | Purpose |
|------|----------|
| `chmod.py` | Modify file permissions |
| `users.py` | List system users |
| `add_user.py` | Add new user |
| `user_login.py` | User authentication |

Implements Unix-style permission handling and user ownership model.

---

### Shell Utilities

| File | Purpose |
|------|----------|
| `history.py` | Show command history |
| `save_command_to_history.py` | Persist commands |
| `exec_cmd_by_num.py` | Execute command by history number |
| `man.py` | Command manual |
| `exit.py` | Exit shell |

---

## Design Characteristics

### 1. Single Responsibility Principle

Each command file:

- Parses its own arguments
- Performs validation
- Executes database logic
- Returns structured response

No command logic is mixed across files.

---

### 2. Decoupled Command Execution

The shell dispatcher dynamically maps user input to:

```
cmd_pkg.<command>
```

This makes adding new commands as simple as:

1. Create a new file
2. Implement the function
3. Register it in dispatcher

---

### 3. Database-Backed Filesystem

All file operations:

- Read from SQLite database
- Write in chunks
- Maintain metadata
- Track ownership
- Enforce permissions

This simulates a persistent filesystem using relational storage.

---

### 4. Permission Enforcement

Commands validate:

- Current user
- File ownership
- Read / Write / Execute bits

Modeled after Linux-style permission system.

---

### 5. History Persistence

Command history is:

- Stored per user
- Saved to database
- Recallable using number execution
- Persisted across sessions

---

## Execution Flow Example

Example:

```
cat file.txt | grep hello | wc -l
```

Flow:

1. Shell parses pipeline
2. Calls:
   - `cat_read.py`
   - `grep.py`
   - `wc.py`
3. Output passed between commands
4. Final result printed

Implements in-memory pipeline chaining.

---

## Extending the System

To add a new command:

1. Create a new Python file in `cmd_pkg`
2. Define the execution function
3. Register it in the command dispatcher
4. Add documentation in `man.py`

No modification required in other commands.

---

## Engineering Value

This folder implements:

- A modular command execution engine
- A database-backed virtual filesystem
- Unix-style permission system
- Persistent multi-user support
- Pipeline command execution
- History recall engine

This architecture scales significantly better than monolithic CLI design.

---

## Possible Improvements

- Dynamic command auto-discovery
- Plugin-based architecture
- Command registration decorator
- Structured logging per command
- Role-based access control
- Group permissions support
- Improved exception hierarchy

---

## Summary

The `cmd_pkg` package represents the core execution layer of the custom shell.

It transforms user commands into structured filesystem operations while enforcing:

- Access control
- Data persistence
- Multi-user isolation
- Modular extensibility

This design mirrors real-world operating system command architecture while leveraging Python and SQLite for persistence.


