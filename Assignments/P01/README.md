# 📁 File System API

A **Unix-like File System simulation** built using **FastAPI + SQLite**.

This project replicates real Linux commands (`ls`, `cd`, `mkdir`, `touch`, `grep`, `chmod`, etc.) using REST APIs and a layered backend architecture. 

It behaves like a **mini virtual operating system** file manager accessible through APIs.

---

## 🚀 Tech Stack

* Python 3.x
* FastAPI
* SQLite
* Uvicorn
* Pydantic

---

## 📂 Project Structure

```
P01/
│
├── config/                 # Configuration handling (.config file logic)
│
├── data/                   # SQLite database (filesystem.db)
│
├── module/                 # Core business logic (Layered Architecture)
│   │
│   ├── cmd_pkg/            # Linux-like command implementations
│   │   ├── ls.py
│   │   ├── cd.py
│   │   ├── mkdir.py
│   │   ├── touch.py
│   │   ├── grep.py
│   │   ├── chmod.py
│   │   ├── rm.py
│   │   ├── rmdir.py
│   │   ├── cp.py
│   │   ├── mv.py
│   │   ├── wc.py
│   │   ├── head.py
│   │   ├── tail.py
│   │   ├── more.py
│   │   ├── less.py
│   │   ├── sort.py
│   │   └── ...
│   │
│   ├── users.py            # User management logic
│   ├── user_login.py       # Authentication logic
│   └── helpers/            # Utility modules
│
├── api.py                  # FastAPI entry point (Presentation Layer)
├── requirements.txt
└── README.md
```

---

## 🏗 Architecture (Layered Design)

This project follows a **3-layer architecture**:

### 1️⃣ Presentation Layer

**`api.py`**

* Defines REST endpoints
* Handles HTTP requests & responses

---

### 2️⃣ Business Logic Layer

**`module/`**

* Contains Linux-style command implementations
* Handles filesystem behavior and validation

---

### 3️⃣ Data Layer

**SQLite Database (`filesystem.db`)**

* Accessed using a CRUD abstraction class
* Stores:

  * Users
  * Files
  * Directories
  * File contents
  * Command history

---

## 🗄 Database Tables

* `users`
* `files`
* `directories`
* `file_contents` (chunk-based BLOB storage)
* `history`

---

## ▶️ How to Run the Project

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Start the Server

```bash
python api.py
```

OR

```bash
uvicorn api:app --reload --port 8080
```

---

### 3️⃣ Open Swagger UI

```
http://127.0.0.1:8080/docs
```

---

## 📌 Available Commands (APIs)

### 📁 File & Directory Commands

| Command | Endpoint | Description              |
| ------- | -------- | ------------------------ |
| ls      | `/ls`    | List files & directories |
| cd      | `/cd`    | Change directory         |
| mkdir   | `/mkdir` | Create directory         |
| touch   | `/touch` | Create file              |
| rm      | `/rm`    | Delete file/directory    |
| rmdir   | `/rmdir` | Delete empty directory   |
| mv      | `/mv`    | Move/Rename              |
| cp      | `/cp`    | Copy file                |
| chmod   | `/chmod` | Change permissions       |

---

### 📄 File Content Commands

| Command | Endpoint     |
| ------- | ------------ |
| cat     | `/cat`       |
| write   | `/cat_write` |
| head    | `/head`      |
| tail    | `/tail`      |
| more    | `/more`      |
| less    | `/less`      |
| wc      | `/wc`        |
| grep    | `/grep`      |
| sort    | `/sort`      |

---

### 👤 User Management

| Function     | Endpoint          |
| ------------ | ----------------- |
| Add user     | `/adduser`        |
| Login        | `/user_login`     |
| List users   | `/users`          |
| Add history  | `/history` (POST) |
| View history | `/history` (GET)  |

---

## 🔐 Permission System

Supports both **numeric** and **symbolic** modes.

### Numeric Mode Examples

```
755
644
777
```

### Symbolic Mode Examples

```
u+x
g-w
o+r
```

Permissions are stored internally as:

* owner_read_permission
* owner_write_permission
* owner_execute_permission
* group_*
* others_*

---

## 🧠 Features

* Unix-like filesystem simulation
* Chunk-based BLOB file storage
* Numeric + symbolic permission system
* Recursive directory deletion
* Pagination (`more`, `less`)
* Regex search (`grep`)
* Sorting support
* Command history tracking
* Config-based session handling

---

## 🔄 Example Workflow

1. Create user → `/adduser`
2. Login → `/user_login`
3. Create directory → `/mkdir`
4. Create file → `/touch`
5. Write content → `/cat_write`
6. List files → `/ls`
7. Change permissions → `/chmod`
8. Delete → `/rm`

---

## 🧪 Development Mode

Run with auto-reload:

```python
uvicorn.run("api:app", host="127.0.0.1", port=8080, reload=True)
```

---

## 📌 Future Improvements

* JWT authentication
* Secure password hashing
* Role-based access control
* Logging system
* Docker support
* Frontend UI

---

## 👨‍💻 Author

**File System API** — Academic Project
Built using FastAPI & SQLite
