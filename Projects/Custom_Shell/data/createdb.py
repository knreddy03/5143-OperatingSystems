import sqlite3

# Database file path
db_path = 'filesystem.db'

# Connect to the SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect(db_path)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Define the schema for the file system with default permissions
create_files_table = """
CREATE TABLE IF NOT EXISTS files (
    file_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    user_id INTEGER,
    size INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    path TEXT NOT NULL,

    -- Owner permissions
    owner_read_permission BOOLEAN DEFAULT 1,  -- Default: Read enabled
    owner_write_permission BOOLEAN DEFAULT 1, -- Default: Write enabled
    owner_execute_permission BOOLEAN DEFAULT 0, -- Default: No execute permission for files

    -- Group permissions
    group_read_permission BOOLEAN DEFAULT 1, -- Default: Read enabled
    group_write_permission BOOLEAN DEFAULT 1, -- Default: Write enabled
    group_execute_permission BOOLEAN DEFAULT 0, -- Default: No execute permission for files

    -- Others permissions
    others_read_permission BOOLEAN DEFAULT 1, -- Default: Read enabled
    others_write_permission BOOLEAN DEFAULT 0, -- Default: No write permission
    others_execute_permission BOOLEAN DEFAULT 0, -- Default: No execute permission for files

    FOREIGN KEY (parent_id) REFERENCES directories(dir_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);"""

create_directories_table = """
CREATE TABLE IF NOT EXISTS directories (
    dir_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    path TEXT NOT NULL,

    -- Owner permissions
    owner_read_permission BOOLEAN DEFAULT 1, -- Default: Read enabled
    owner_write_permission BOOLEAN DEFAULT 1, -- Default: Write enabled
    owner_execute_permission BOOLEAN DEFAULT 1, -- Default: Execute enabled (for directories)

    -- Group permissions
    group_read_permission BOOLEAN DEFAULT 1, -- Default: Read enabled
    group_write_permission BOOLEAN DEFAULT 1, -- Default: Write enabled
    group_execute_permission BOOLEAN DEFAULT 1, -- Default: Execute enabled (for directories)

    -- Others permissions
    others_read_permission BOOLEAN DEFAULT 1, -- Default: Read enabled
    others_write_permission BOOLEAN DEFAULT 0, -- Default: No write permission
    others_execute_permission BOOLEAN DEFAULT 1, -- Default: Execute enabled (for directories)

    FOREIGN KEY (parent_id) REFERENCES directories(dir_id), -- Self-referencing for subdirectories
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);"""

create_file_contents_table = """
CREATE TABLE IF NOT EXISTS file_contents (
    content_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    chunk BLOB, -- Each file's content is split into chunks for efficient storage
    chunk_index INTEGER,
    FOREIGN KEY (file_id) REFERENCES files(file_id)
);"""

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""

create_history_table = """
CREATE TABLE IF NOT EXISTS history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    commands TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);"""

create_man_commands_table = """
CREATE TABLE IF NOT EXISTS mans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command_name TEXT NOT NULL,
    man_command TEXT NOT NULL
    FOREIGN KEY (id) REFERENCES user(user_id)
);"""

# Execute the table creation queries
cursor.execute(create_files_table)
cursor.execute(create_directories_table)
cursor.execute(create_file_contents_table)
cursor.execute(create_users_table)
cursor.execute(create_history_table)
cursor.execute(create_man_commands_table)


# Insert default users
cursor.executescript("""
INSERT INTO users (username, password) VALUES
    ('root', 'password0'),
    ('bob', 'password1'),
    ('mia', 'password2'),
    ('raj', 'password3')
ON CONFLICT(username) DO NOTHING;  -- Prevents inserting duplicates
""")


# Commit the changes
conn.commit()

# Close the connection when done
conn.close()

print("File system schema with default permissions created successfully!")
