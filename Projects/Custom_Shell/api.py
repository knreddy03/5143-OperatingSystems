# Libraries for FastAPI
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os, re, math
from pydantic import BaseModel
from datetime import datetime
from config.config import load_config, save_config


# Classes from my module
# from module import SqliteCRUD
from module import *

CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class WriteFileRequest(BaseModel):
    file_path: str
    content: str
    user_id: int
    append: bool = False  # Append is False by default, meaning overwrite


# """
#            _____ _____   _____ _   _ ______ ____
#      /\   |  __ \_   _| |_   _| \ | |  ____/ __ \\
#     /  \  | |__) || |     | | |  \| | |__ | |  | |
#    / /\ \ |  ___/ | |     | | | . ` |  __|| |  | |
#   / ____ \| |    _| |_   _| |_| |\  | |   | |__| |
#  /_/    \_\_|   |_____| |_____|_| \_|_|    \____/

# The `description` is the information that gets displayed when the api is accessed from a browser and loads the base route.
# Also the instance of `app` below description has info that gets displayed as well when the base route is accessed.
# /

description = """🚀
## File System Api
"""


# This is the `app` instance which passes in a series of keyword arguments
# configuring this instance of the api. The URL's are obviously fake.
app = FastAPI(
    title="File System",
    description=description,
    version="0.0.1",
    terms_of_service="https://profgriffin.com/terms/",
    contact={
        "name": "FileSystemAPI",
        "url": "https://profgriffin.com/contact/",
        "email": "chacha@profgriffin.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# """
#   _      ____   _____          _         _____ _                _____ _____ ______  _____
#  | |    / __ \ / ____|   /\   | |       / ____| |        /\    / ____/ ____|  ____|/ ____|
#  | |   | |  | | |       /  \  | |      | |    | |       /  \  | (___| (___ | |__  | (___
#  | |   | |  | | |      / /\ \ | |      | |    | |      / /\ \  \___ \\___ \|  __|  \___ \\
#  | |___| |__| | |____ / ____ \| |____  | |____| |____ / ____ \ ____) |___) | |____ ____) |
#  |______\____/ \_____/_/    \_\______|  \_____|______/_/    \_\_____/_____/|______|_____/

# This is where you will add code to load all the countries and not just countries. Below is a single
# instance of the class `CountryReader` that loads countries. There are 6 other continents to load or
# maybe you create your own country file, which would be great. But try to implement a class that
# organizes your ability to access a countries polygon data.
# """


dataPath = "./data/"
dbName = "filesystem.db"
if os.path.exists(os.path.join(dataPath, dbName)):
    fsDB = SqliteCRUD(os.path.join(dataPath, dbName))
else:
    print("Database file not found.")
    fsDB = None

config_data = load_config()  # Call the function to load config


# """
#   _      ____   _____          _        __  __ ______ _______ _    _  ____  _____   _____
#  | |    / __ \ / ____|   /\   | |      |  \/  |  ____|__   __| |  | |/ __ \|  __ \ / ____|
#  | |   | |  | | |       /  \  | |      | \  / | |__     | |  | |__| | |  | | |  | | (___
#  | |   | |  | | |      / /\ \ | |      | |\/| |  __|    | |  |  __  | |  | | |  | |\___ \\
#  | |___| |__| | |____ / ____ \| |____  | |  | | |____   | |  | |  | | |__| | |__| |____) |
#  |______\____/ \_____/_/    \_\______| |_|  |_|______|  |_|  |_|  |_|\____/|_____/|_____/

# I place local methods either here, or in the module we created. I'm leaving it here to help
# with the lecture we had in class, but it can easily be moved then imported. In fact you should
# move it if you have other "spatial" methods that it can be packaged with in the module folder.
# """


def split_binary_file_to_chunks(file_path, chunk_size=1024):
    chunks = []

    with open(file_path, "rb") as file:
        while True:
            # Read a chunk of size `chunk_size`
            chunk = file.read(chunk_size)
            if not chunk:
                break  # End of file
            chunks.append(chunk)

    return chunks


def split_file_to_chunks(file_path, chunk_size=1024, encoding="utf-8"):
    chunks = []

    with open(file_path, "r", encoding=encoding) as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break  # End of file
            chunks.append(chunk)

    return chunks


# """
#   _____   ____  _    _ _______ ______  _____
#  |  __ \ / __ \| |  | |__   __|  ____|/ ____|
#  | |__) | |  | | |  | |  | |  | |__  | (___
#  |  _  /| |  | | |  | |  | |  |  __|  \___ \\
#  | | \ \| |__| | |__| |  | |  | |____ ____) |
#  |_|  \_\\____/ \____/   |_|  |______|_____/

#  This is where your routes will be defined. Remember they are really just python functions
#  that will talk to whatever class you write above. Fast Api simply takes your python results
#  and packagres them so they can be sent back to your programs request.
# """


@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")


@app.get("/files/")
async def getFiles(did: int, user_id: int):
    """
    ### Description:
        Get a list of files in the current directory.
    ### Params:
        did (int) : directory id to list files from (optional)
    ### Returns:
        list : of files in the directory or all files if did is None
    """
    # Fetch all files
    files = fsDB.readData("files")
    
    if files['success']:
        # If `did` is provided, filter the files by directory id (using 'parent_id' key instead of index)
        if did is not None:
            filtered_files = [file for file in files["data"] if file["parent_id"] == did and file["user_id"] == user_id]  # Access using dictionary key
            return filtered_files if filtered_files else {"Error": "No files found in this directory."}
        
        # # If no `did` is provided, return all files
        # return files["data"]
    
    return {"Error": "Files list was empty or None."}


@app.get("/directories/")
async def getDirectories(did: int, user_id: int):
    """
    ### Description:
        Get a list of directories in the current directory.
    ### Params:
        did (int) : directory id to list directories from (optional)
    ### Returns:
        list : of directories in the directory or all directories if did is None
    """
    # Fetch all directories
    directories = fsDB.readData("directories")
    
    if directories['success']:
        # If `did` is provided, filter the directories by directory id (using 'parent_id' key instead of index)
        if did is not None:
            filtered_directories = [directory for directory in directories["data"] if directory["parent_id"] == did and directory["user_id"] == user_id]  # Access using dictionary key
            return filtered_directories if filtered_directories else {"Error": "No directories found in this directory."}
        
        # # If no `did` is provided, return all directories
        # return directories["data"]
    
    return {"Error": "directories list was empty or None."}


@app.get("/path")
async def get_details_with_path(path: str, user_id: int):
    """
    ### Description:
        List files and directories in the specified directory.
    ### Params:
        path (int) : directory id to list files and directories from.
    ### Returns:
        dict : containing lists of files and directories, or an error message.
    """
    # Fetch all files and directories
    files_response = fsDB.readData("files")
    directories_response = fsDB.readData("directories")

    # Check if files fetch was successful
    if not files_response['success']:
        return {"Error": "Files list was empty or None."}

    # Check if directories fetch was successful
    if not directories_response['success']:
        return {"Error": "Directories list was empty or None."}

    # Filter files based on directory ID and user ID
    filtered_files = [
        file for file in files_response["data"]
        if file["path"] == path and file["user_id"] == user_id
    ]

    # Filter directories based on directory ID and user ID
    filtered_directories = [
        directory for directory in directories_response["data"]
        if directory["path"] == path and directory["user_id"] == user_id
    ]

    return {
        "files": filtered_files if filtered_files else [],
        "directories": filtered_directories if filtered_directories else []
    }


@app.get("/parent")
async def parent_details(parent_id: int, user_id: int):
    """
    ### Description:
        List directories in the specified directory.
    ### Params:
        directory_id (int) : directory id to list files and directories from.
    ### Returns:
        dict : containing lists of directories, or an error message.
    """
    # Fetch alldirectories
    directories_response = fsDB.readData("directories")

    # Check if directories fetch was successful
    if not directories_response['success']:
        return {"Error": "Directories list was empty or None."}

    # Filter directories based on directory ID and user ID
    
    for directory in directories_response["data"]:
        if directory["dir_id"] == parent_id and directory["user_id"] == user_id:
            filtered_directories = directory
    
    return filtered_directories if filtered_directories else []
    

@app.get("/users/")
async def getUsers(user_id: int = None):
    """
    ### Description:
        Get a list of users in the current system.
    ### Params:
        did (int) : directory id to list files from (optional)
    ### Returns:
        list : of files in the directory or all files if did is None
    """
    # Fetch all files
    users = fsDB.readData("users")
    
    if users['success']:
        # If `did` is provided, filter the users by directory id (using 'parent_id' key instead of index)
        if user_id is not None:
            filtered_users = [user for user in users["data"] if user["user_id"] == user_id]  # Access using dictionary key
            return filtered_users if filtered_users else {"Error": "No users found in this directory."}
        
        # If no `did` is provided, return all users
        return users["data"]
    
    return {"Error": "users list was empty or None."}


def format_permissions(item, is_directory=False):
    """
    Convert binary permissions to rwx format.
    
    Args:
        item (dict): A dictionary representing a file or directory record.
        is_directory (bool): True if the item is a directory, otherwise False.
    
    Returns:
        str: Formatted permissions string.
    """
    permissions = "d" if is_directory else "-"
    permissions += "r" if item["owner_read_permission"] else "-"
    permissions += "w" if item["owner_write_permission"] else "-"
    permissions += "x" if item["owner_execute_permission"] else "-"
    permissions += "r" if item["group_read_permission"] else "-"
    permissions += "w" if item["group_write_permission"] else "-"
    permissions += "x" if item["group_execute_permission"] else "-"
    permissions += "r" if item["others_read_permission"] else "-"
    permissions += "w" if item["others_write_permission"] else "-"
    permissions += "x" if item["others_execute_permission"] else "-"
    return permissions

def human_readable_size(size):
    """
    Converts a file size in bytes to a human-readable format (e.g., KB, MB).
    
    Args:
        size (int): Size in bytes.
    
    Returns:
        str: Human-readable size.
    """
    if size < 1024:
        return f"{size}B"
    elif size < 1024 ** 2:
        return f"{size / 1024:.1f}K"
    elif size < 1024 ** 3:
        return f"{size / 1024 ** 2:.1f}M"
    elif size < 1024 ** 4:
        return f"{size / 1024 ** 3:.1f}G"
    else:
        return f"{size / 1024 ** 4:.1f}T"

@app.get("/ls")
async def get_files_and_directories(
    did: int,
    user_id: int,
    show_hidden: bool = False,
    detailed: bool = False,
    human_readable: bool = False
):
    """
    List files and directories in the specified directory with options for showing hidden files,
    detailed information, and human-readable size formatting.
    
    Parameters:
    - did (int): Directory ID to list files and directories from.
    - user_id (int): ID of the user requesting the contents.
    - show_hidden (bool): If True, includes hidden files (files that start with '.').
    - detailed (bool): If True, includes detailed file information.
    - human_readable (bool): If True, shows sizes in a human-readable format.
    
    Returns:
    - dict: Contains lists of files and directories, or an error message.
    """
    files_response = fsDB.readData("files")
    directories_response = fsDB.readData("directories")

    if not files_response['success'] or not files_response['data']:
        files_response['data'] = []

    if not directories_response['success'] or not directories_response['data']:
        directories_response['data'] = []

    # Filter files and directories by directory ID (did) and user ID (user_id)
    def filter_items(items, parent_id):
        return [
            item for item in items
            if item["parent_id"] == parent_id
            and item["user_id"] == user_id
            and (not item["name"].startswith(".") or (show_hidden))
        ]

    total_size = 0  # Initialize total size for all items
    result = {
        "total": "",  # This will be set at the end
        "directories": [],
        "files": []
    }

    # Generate result for directories
    for directory in filter_items(directories_response["data"], did):
        size = 4096  # Default size for directories
        total_size += size
        if detailed or human_readable or show_hidden:
            permissions = format_permissions(directory, is_directory=True)
            formatted_size = human_readable_size(size) if human_readable else size
            result["directories"].append({
                "name": directory["name"],
                "permissions": permissions,
                "owner": "user",
                "group": "group",
                "size": formatted_size,
                "created_at": directory["created_at"],
                "modified_at": directory["modified_at"]
            })
        else:
            result["directories"].append({"name": directory["name"]})

    # Generate result for files
    for file in filter_items(files_response["data"], did):
        size = file["size"]
        total_size += size
        if detailed or human_readable or show_hidden:
            permissions = format_permissions(file, is_directory=False)
            formatted_size = human_readable_size(size) if human_readable else size
            result["files"].append({
                "name": file["name"],
                "permissions": permissions,
                "owner": "user",
                "group": "group",
                "size": formatted_size,
                "created_at": file["created_at"],
                "modified_at": file["modified_at"]
            })
        else:
            result["files"].append({"name": file["name"]})

    # Set the total size in a human-readable format if requested
    result["total"] = human_readable_size(total_size) if human_readable else total_size

    return result


@app.post("/touch")
async def create_file(name: str, parent_id: int, user_id: int, path: str):
    """
    Creates a new file in the filesystem and records the action in the database.
    """
    if fsDB is None:
        raise HTTPException(status_code=500, detail="Database not connected.")
    
    files_in_directory = fsDB.readData("files")
    
    # Step 2: Check if file already exists
    for file in files_in_directory["data"]:
        if file["name"] == name and file["parent_id"] == parent_id and file["user_id"] == user_id:
            raise HTTPException(status_code=400, detail="File already exists in the directory.")
    
    created_at = modified_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    size = 0  # Initial size of the new file
    
    try:
        # Insert the new file into the database
        fsDB.insertData(
            "files", (None, name, parent_id, user_id, size, created_at, modified_at, path, 1, 1, 0, 1, 1, 0, 1, 0, 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": f"File '{name}' successfully created in directory {parent_id}."}


@app.post("/mkdir")
async def create_directory(name: str, parent_id: int, user_id: int, path: str):
    """
    Creates a new directory in the filesystem and records the action in the database.
    """
    if fsDB is None:
        raise HTTPException(status_code=500, detail="Database not connected.")
    
    directories = fsDB.readData("directories")
    
    # Step 2: Check if directory already exists
    for directory in directories["data"]:
        if directory["name"] == name and directory["parent_id"] == parent_id and directory["user_id"] == user_id:
            raise HTTPException(status_code=400, detail="Directory already exists in the directory.")
    
    created_at = modified_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # Insert the new directory into the database
        fsDB.insertData(
            "directories", (None, name, parent_id, user_id, created_at, modified_at, path, 1, 1, 1, 1, 1, 1, 1, 0, 1)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": f"Directory '{name}' successfully created in directory {parent_id}."}


@app.post("/adduser")
async def create_user(username: str, password: str):
    """
    Creates a new file in the filesystem and records the action in the database.
    """
    if fsDB is None:
        raise HTTPException(status_code=500, detail="Database not connected.")
    
    users = fsDB.readData("users")
    
    # Step 2: Check if file already exists
    for user in users["data"]:
        if user["username"] == username and user["password"] == password:
            raise HTTPException(status_code=400, detail="User already exists.")
    
    modified_at = created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # Insert the new file into the database
        fsDB.insertData(
            "users", (None, username, password, created_at)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    name = "home"
    path = f"/home/{username}"
    users = fsDB.readData("users")
    for user in users["data"]:
        if user["username"] == username:
            fsDB.insertData(
                "directories", (None, name, 1, user["user_id"], created_at, modified_at, path, 1, 1, 1, 1, 1, 1, 1, 0, 1)
                )
    return {"message": f"User '{username}' successfully created with password {password}."}


@app.post("/user_login")
async def user_login(username: str, password: str):
    """
    Handles user login by checking credentials and updating the current directory.
    """
    if fsDB is None:
        raise HTTPException(status_code=500, detail="Database not connected.")
    
    users = fsDB.readData("users")
    directories = fsDB.readData("directories")
    
    # Check if the user exists and the password is correct
    for user in users["data"]:
        if user["username"] == username:
            if user["password"] == password:
                
                config = load_config()  # Load current .config file
                    
                # Set new values for current user, user id, and home directory
                config["Settings"]["current_user"] = username
                config["Settings"]["current_user_id"] = user["user_id"]
                config["Settings"]["current_directory"] = f"/home/{username}"  # Assuming the home dir is /home/{username}
                save_config(config)  # Save updated config
            
                for directory in directories["data"]:
                    if user["user_id"] == directory["user_id"] and directory["path"] == config["Settings"]["current_directory"]:
                        config["Settings"]["current_directory_id"] = directory["dir_id"]
                        config["Settings"]["parent_id"] = directory["parent_id"]

                        save_config(config)  # Save updated config
                
                return {"message": f"User '{username}' logged in successfully."}
                
            else:
                raise HTTPException(status_code=400, detail="Incorrect password.")
    
    raise HTTPException(status_code=404, detail="User not found.")


@app.get("/cd")
async def change_directory(directory_id: int, user_id: int):
    """
    Returns the contents of a specified directory based on directory_id and user_id.
    This route is used for navigating into a directory.
    """
    # Fetch all directories
    directories_response = fsDB.readData("directories")

    # Check if directories fetch was successful
    if not directories_response['success']:
        return {"Error": "Directories list was empty or None."}

    # Filter to find the specified directory by `directory_id` and `user_id`
    target_directory = [
        directory for directory in directories_response["data"]
        if directory["dir_id"] == directory_id and directory["user_id"] == user_id
    ]
    
    if not target_directory:
        return {"Error": "Directory not found or access is restricted."}

    # Retrieve subdirectories within the target directory
    subdirectories = [
        sub_dir for sub_dir in directories_response["data"]
        if sub_dir["parent_id"] == directory_id and sub_dir["user_id"] == user_id
    ]

    return {
        "directory": target_directory[0],
        "subdirectories": subdirectories
    }


@app.get("/grep")
async def grep_file(
    file_path: str, 
    user_id: int, 
    pattern: str, 
    ignore_case: bool = False, 
    count_only: bool = False, 
    word_match: bool = False
):
    """
    Searches for a pattern in the file's content and highlights matched words in red.
    """
    file_record = next((f for f in fsDB.readData("files")["data"] if f["path"] == file_path and f["user_id"] == user_id), None)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found or access denied.")

    # Check write permissions
    if not file_record["owner_read_permission"]:
        raise HTTPException(status_code=403, detail="User does not have read permission for this file.")

    # Read and reconstruct content
    file_chunks = fsDB.readFileData("file_contents", file_record["file_id"])["data"]
    content = "".join(chunk["chunk"].decode("utf-8") for chunk in file_chunks).splitlines()

    # Prepare search options
    flags = re.IGNORECASE if ignore_case else 0
    pattern = f"\\b{pattern}\\b" if word_match else pattern
    matches = []

    # ANSI escape codes for red color
    red_start = "\033[91m"
    reset_color = "\033[0m"

    # Search each line
    for line in content:
        if re.search(pattern, line, flags):
            # Highlight the matched words in red
            highlighted_line = re.sub(
                pattern, 
                lambda match: f"{red_start}{match.group(0)}{reset_color}", 
                line, 
                flags=flags
            )
            matches.append(highlighted_line)

    if count_only:
        return {"count": len(matches)}
    return {"matches": matches}


@app.get("/dirId")
def getDirId(dir: str, pid: int = 1):
    """
    Get the directory id by name
    @args:
        dir: str - the name of the directory
        pid: int - the parent id of the directory
    @returns:
        int - the id of the directory or response with error
    """
    dirs = dir.strip().rstrip("/").split("/")

    query = f"SELECT id FROM directories WHERE name = '{dirs[0]}' and pid = '{pid}'"

    res = fsDB.run_query_in_thread([query])[0]

    if res["success"]:
        if len(res["data"]) > 0:
            pid = res["data"][0][0]
        else:
            res["message"] = f"Directory {dirs[0]} not found."
            return res
    else:
        return res
    if len(dirs) > 1:
        for dir in dirs[1:]:
            print(f"dir: {dir}")
            query = f"SELECT id FROM directories WHERE name = '{dir}' and pid = '{pid}'"
            res = fsDB.run_query_in_thread([query])[0]
            if res["success"]:
                if len(res["data"]) > 0:
                    pid = res["data"][0][0]
                else:
                    res["message"] = f"Directory {dir} not found."
                    return res
            else:
                return res
    return pid


@app.delete("/rm")
async def delete_path(path: str, user_id: int, recursive: bool = False):
    """
    Deletes a file or directory from the filesystem.
    - If the path is a file, delete it.
    - If the path is a directory and `recursive` is False, raise an error.
    - If the path is a directory and `recursive` is True, delete all sub-files and subdirectories.

    Parameters:
    - path (str): Path of the file or directory to delete.
    - user_id (int): ID of the user performing the deletion.
    - recursive (bool): If True, delete directories and their contents recursively.
    """
    if fsDB is None:
        raise HTTPException(status_code=500, detail="Database not connected.")

    # Step 1: Check if the path exists in files or directories
    file_data = fsDB.readData("files")
    file_path = next((f for f in file_data["data"] if f["path"] == path and f["user_id"] == user_id), None)

    # If not found in files, check directories
    if not file_path:
        dir_data = fsDB.readData("directories")
        dir_path = next((d for d in dir_data["data"] if d["path"] == path and d["user_id"] == user_id), None)
    else:
        dir_path = None

    # If neither file nor directory exists, raise an error
    if not file_path and not dir_path:
        raise HTTPException(status_code=404, detail="Path not found or not accessible by the user.")

    # Step 2: If the path is a file, delete it
    if file_path:
        # Check write permissions
        if not file_path.get("owner_write_permission"):
            raise HTTPException(status_code=403, detail="User does not have write permission for this file.")
        try:
            fsDB.deleteData("files", "file_id", file_path["file_id"])
            return {"message": f"File '{path}' successfully deleted."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

    # Step 3: If the path is a directory
    if dir_path:
        # Check write and execute permissions
        if not (dir_path.get("owner_write_permission") and dir_path.get("owner_execute_permission")):
            raise HTTPException(status_code=403, detail="User does not have sufficient permissions to delete this directory.")

        if not recursive:
            # Non-recursive deletion of a directory: raise an error
            raise HTTPException(status_code=400, detail="Cannot remove: given path is a directory. Use recursive=True to delete a directory and its contents.")

        # Recursive deletion
        try:
            # Build a regex pattern to match the current directory and all its sub-paths
            pattern = re.compile(f"^{re.escape(path)}(/.*)?$")

            # Step 3.1: Retrieve and delete all files within the directory
            files_to_delete = [f for f in file_data["data"] if pattern.match(f["path"]) and f["user_id"] == user_id]
            for file in files_to_delete:
                fsDB.deleteData("files", "file_id", file["file_id"])

            # Step 3.2: Retrieve and delete all subdirectories within the directory
            directories_to_delete = [d for d in dir_data["data"] if pattern.match(d["path"]) and d["user_id"] == user_id]
            for directory in sorted(directories_to_delete, key=lambda d: d["path"], reverse=True):
                fsDB.deleteData("directories", "dir_id", directory["dir_id"])

            # Finally, delete the target directory
            fsDB.deleteData("directories", "dir_id", dir_path["dir_id"])

            return {"message": f"Directory '{path}' and all its contents successfully deleted."}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting directory: {str(e)}")


@app.delete("/rmdir")
async def delete_empty_directory(path: str, user_id: int):
    """
    Deletes an empty directory from the filesystem.
    - If the directory contains files or subdirectories, returns an error.
    
    Parameters:
    - path (str): Path of the directory to delete.
    - user_id (int): ID of the user performing the deletion.
    """
    if fsDB is None:
        raise HTTPException(status_code=500, detail="Database not connected.")

    # Check if the directory exists and belongs to the user
    directories = fsDB.readData("directories")
    target_dir = next((d for d in directories["data"] if d["path"] == path and d["user_id"] == user_id), None)
    
    if not target_dir:
        raise HTTPException(status_code=404, detail="Directory not found or not accessible by the user.")

    # Check write and execute permissions on the parent directory
    parent_id = target_dir["parent_id"]
    parent_dir = next((d for d in directories["data"] if d["dir_id"] == parent_id and d["user_id"] == user_id), None)

    if not parent_dir or not (parent_dir["owner_write_permission"] and parent_dir["owner_execute_permission"]):
        raise HTTPException(
            status_code=403,
            detail="User does not have sufficient permissions on the parent directory to remove this directory."
        )

    # Check if the directory is empty (no files or subdirectories)
    dir_id = target_dir["dir_id"]
    files_in_directory = [f for f in fsDB.readData("files")["data"] if f["parent_id"] == dir_id]
    subdirectories_in_directory = [d for d in directories["data"] if d["parent_id"] == dir_id]

    if files_in_directory or subdirectories_in_directory:
        raise HTTPException(status_code=400, detail="Directory is not empty.")

    # If empty, delete the directory
    try:
        fsDB.deleteData("directories", "dir_id", dir_id)
        return {"message": f"Directory '{path}' deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while deleting the directory: {str(e)}")


@app.get("/cat")
async def cat_file(file_path: str, user_id: int):
    """
    Fetch the content of a file line by line.
    """
    # Fetch file record
    file_record = next((f for f in fsDB.readData("files")["data"] if f["path"] == file_path and f["user_id"] == user_id), None)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found or access denied.")
    
    # Check write permissions
    if not file_record["owner_read_permission"]:
        raise HTTPException(status_code=403, detail="User does not have read permission for this file.")

    # Read and reconstruct file content
    file_chunks = fsDB.readFileData("file_contents", file_record["file_id"])["data"]
    content = "".join(chunk["chunk"].decode("utf-8") for chunk in file_chunks).splitlines()

    return {"lines": content}  # Return content as a list of lines


@app.post("/cat_write")
async def cat_write(
    file_path: str,
    user_id: int,
    content: str,
    append: bool = False
):
    """
    Writes content to a file, either appending or overwriting it.
    """
    # Fetch the file record
    file_record = next(
        (f for f in fsDB.readData("files")["data"] if f["path"] == file_path and f["user_id"] == user_id),
        None,
    )
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found or access denied.")

    # Check write permissions
    if not file_record["owner_write_permission"]:
        raise HTTPException(status_code=403, detail="User does not have write permission for this file.")

    try:
        # Retrieve existing content if appending
        existing_chunks = []
        if append:
            existing_chunks = fsDB.readFileData("file_contents", file_record["file_id"])["data"]

        # Combine existing content (if appending) with new content
        all_content = (
            "".join(chunk["chunk"].decode("utf-8") for chunk in existing_chunks)
            + ("\n" if existing_chunks else "")  # Add newline if appending
            + content
        ) if append else content

        # Write new content in chunks
        fsDB.deleteData("file_contents", "file_id", file_record["file_id"])  # Clear old chunks if overwriting
        chunk_size = 1024  # Chunk size
        for i in range(0, len(all_content), chunk_size):
            chunk = all_content[i:i + chunk_size].encode("utf-8")
            fsDB.insertData("file_contents", (None, file_record["file_id"], chunk, i // chunk_size))

        # Update file size
        fsDB.updateData("files", "size", len(all_content), "file_id", file_record["file_id"])
        return {"message": f"Content {'appended to' if append else 'written to'} file '{file_path}' successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@app.post("/history")
async def add_command_to_history(user_id: int, command: str):
    """
    Logs a command to the history table.
    
    Parameters:
    - entry (HistoryEntry): Contains `user_id` and `command`.
    """
    if fsDB is None:
        raise HTTPException(status_code=500, detail="Database not connected.")
    
    # Insert the command into history
    try:
        fsDB.insertData("history", (None, user_id, command))
        return {"message": "Command added to history successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/history")
async def get_command_history(user_id: int):
    """
    Retrieves the command history for a user.
    
    Parameters:
    - user_id (int): ID of the user whose history is requested.
    """
    if fsDB is None:
        raise HTTPException(status_code=500, detail="Database not connected.")
    
    # Retrieve history for the user
    try:
        history_records = [
            {"command": record["command"], "history_id": record["history_id"]}
            for record in fsDB.readData("history")["data"]
            if record["user_id"] == user_id
        ]
        return {"history": history_records}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/head")
async def head(file_path: str, user_id: int, lines: int):
    """
    Fetch the first `n` lines of a file stored in BLOB format.
    """
    file_record = next((f for f in fsDB.readData("files")["data"] if f["path"] == file_path and f["user_id"] == user_id), None)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found or access denied.")

    # Read and reconstruct content
    file_chunks = fsDB.readFileData("file_contents", file_record["file_id"])["data"]
    content = "".join(chunk["chunk"].decode("utf-8") for chunk in file_chunks).splitlines()

    # Fetch first `n` lines
    head_content = "\n".join(content[:lines])
    return {"content": head_content}


@app.get("/tail")
async def tail(file_path: str, user_id: int, lines: int):
    """
    Fetch the last `n` lines of a file stored in BLOB format.
    """
    file_record = next((f for f in fsDB.readData("files")["data"] if f["path"] == file_path and f["user_id"] == user_id), None)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found or access denied.")

    # Read and reconstruct content
    file_chunks = fsDB.readFileData("file_contents", file_record["file_id"])["data"]
    content = "".join(chunk["chunk"].decode("utf-8") for chunk in file_chunks).splitlines()

    # Fetch last `n` lines
    tail_content = "\n".join(content[-lines:])
    return {"content": tail_content}


### 5. **File Rename**
@app.post("/mv")
async def move_file_or_directory(source_path: str, destination_path: str, user_id: int):
    """
    Moves a file or directory from source to destination.
    """
    try:
        # Fetch the source file record
        source_record = next(
            (f for f in fsDB.readData("files")["data"] if f["path"] == source_path and f["user_id"] == user_id),
            None
        )
        if not source_record:
            raise HTTPException(status_code=404, detail="Source file not found or access denied.")

        # Check if the destination is a directory
        destination_directory = next(
            (d for d in fsDB.readData("directories")["data"] if d["path"] == destination_path.rstrip('/') and d["user_id"] == user_id),
            None
        )

        if destination_directory:
            # If destination is a directory, append source filename
            destination_path = f"{destination_path.rstrip('/')}/{source_record['name']}"
            parent_id = destination_directory["dir_id"]
        else:
            # If destination is a file, set parent_id to source's parent_id
            parent_id = source_record["parent_id"]

        # Check if the destination already exists
        destination_record = next(
            (f for f in fsDB.readData("files")["data"] if f["path"] == destination_path and f["user_id"] == user_id),
            None
        )
        modified_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if destination_record:
            # Overwrite destination if it exists
            fsDB.deleteData("file_contents", "file_id", destination_record["file_id"])
            fsDB.updateData("files", "modified_at", modified_at, "file_id", destination_record["file_id"])
        else:
            # Create a new file record for the destination
            fsDB.insertData("files", (
                None,
                destination_path.split('/')[-1],
                parent_id,
                user_id,
                source_record["size"],
                source_record["created_at"],
                modified_at,
                destination_path,
                source_record["owner_read_permission"],
                source_record["owner_write_permission"],
                source_record["owner_execute_permission"],
                source_record["group_read_permission"],
                source_record["group_write_permission"],
                source_record["group_execute_permission"],
                source_record["others_read_permission"],
                source_record["others_write_permission"],
                source_record["others_execute_permission"]
            ))

            destination_record = next(
                (f for f in fsDB.readData("files")["data"] if f["path"] == destination_path and f["user_id"] == user_id),
                None
            )

        # Copy content from source to destination
        source_chunks = fsDB.readFileData("file_contents", source_record["file_id"])["data"]
        for index, chunk in enumerate(source_chunks):
            fsDB.insertData("file_contents", (None, destination_record["file_id"], chunk["chunk"], index))

        # Delete the source file and its contents after copying
        fsDB.deleteData("file_contents", "file_id", source_record["file_id"])
        fsDB.deleteData("files", "file_id", source_record["file_id"])

        return

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


### 8. **Line Count**
@app.get("/wc")
async def wc(file_path: str, user_id: int, count_type: str = 'lines'):
    """
    Counts lines, words, or characters in a file stored in BLOB format.
    """
    file_record = next((f for f in fsDB.readData("files")["data"] if f["path"] == file_path and f["user_id"] == user_id), None)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found or access denied.")

    # Read and decode file content
    file_chunks = fsDB.readFileData("file_contents", file_record["file_id"])["data"]
    content = "".join(chunk["chunk"].decode("utf-8") for chunk in file_chunks)

    if count_type == 'lines':
        return {"count": len(content.splitlines())}
    elif count_type == 'words':
        return {"count": len(content.split())}
    elif count_type == 'chars':
        return {"count": len(content)}
    else:
        raise HTTPException(status_code=400, detail="Invalid count type. Use 'lines', 'words', or 'chars'.")

        
### 9. **File Copy**
@app.post("/cp")
async def copy_file_or_directory(source_path: str, destination_path: str, user_id: int):
    """
    Copies a file or directory from source to destination.
    """
    try:
        # Fetch the source file record
        source_record = next(
            (f for f in fsDB.readData("files")["data"] if f["path"] == source_path and f["user_id"] == user_id),
            None
        )
        if not source_record:
            raise HTTPException(status_code=404, detail="Source file not found or access denied.")

        # Check if the destination is an existing directory
        destination_directory = next(
            (d for d in fsDB.readData("directories")["data"] if d["path"] == destination_path.rstrip('/') and d["user_id"] == user_id),
            None
        )

        if destination_directory:
            # If copying into a directory, add the source file name to the destination path
            destination_path = f"{destination_path.rstrip('/')}/{source_record['name']}"
            parent_id = destination_directory["dir_id"]
        else:
            # Otherwise, keep the original parent_id from the source
            parent_id = source_record['parent_id']

        # Check if the destination file already exists
        destination_record = next(
            (f for f in fsDB.readData("files")["data"] if f["path"] == destination_path and f["user_id"] == user_id),
            None
        )

        created_at = modified_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not destination_record:
            # Insert a new record for the destination file
            insert_result = fsDB.insertData("files", (
                None,
                source_record['name'],
                parent_id,
                user_id,
                source_record['size'],
                created_at,
                modified_at,
                destination_path,
                source_record['owner_read_permission'],
                source_record['owner_write_permission'],
                source_record['owner_execute_permission'],
                source_record['group_read_permission'],
                source_record['group_write_permission'],
                source_record['group_execute_permission'],
                source_record['others_read_permission'],
                source_record['others_write_permission'],
                source_record['others_execute_permission']
            ))
            if not insert_result["success"]:
                raise HTTPException(status_code=500, detail="Failed to insert destination file record.")

            # Fetch the newly created destination record
            destination_record = next(
                (f for f in fsDB.readData("files")["data"] if f["path"] == destination_path and f["user_id"] == user_id),
                None
            )

        # Read source file content in chunks
        source_chunks = fsDB.readFileData("file_contents", source_record["file_id"])["data"]
        if not source_chunks:
            raise HTTPException(status_code=404, detail="Source file content not found.")

        # Delete existing content if the destination already exists
        if destination_record:
            fsDB.deleteData("file_contents", "file_id", destination_record["file_id"])
            fsDB.updateData("files", "modified_at", modified_at, "file_id", destination_record["file_id"])

        # Insert copied chunks into the destination file
        for index, chunk in enumerate(source_chunks):
            fsDB.insertData("file_contents", (None, destination_record["file_id"], chunk["chunk"], index))

        return 

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/more")
async def more_api(
    file_path: str,
    user_id: int,
    next_page: int = Query(1, ge=1)  # Default to the first page
):
    """
    Paginate file content for the `more` command.

    Args:
        file_name (str): The path of the file.
        user_id (int): The ID of the user requesting the file.
        next_page (int): The page number to display (default is 1).
    
    Returns:
        JSON response with the requested page and metadata.
    """
    lines_per_page = 10  # Default number of lines per page

    # Simulate fetching file record
    file_record = next(
        (f for f in fsDB.readData("files")["data"] if f["path"] == file_path and f["user_id"] == user_id), 
        None
    )
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found or access denied.")

    # Fetch file content
    file_content = [
        chunk["chunk"].decode("utf-8") 
        for chunk in fsDB.readFileData("file_contents", file_record["file_id"])["data"]
    ]
    all_lines = "\n".join(file_content).splitlines()

    # Calculate total pages and validate next_page
    total_lines = len(all_lines)
    total_pages = math.ceil(total_lines / lines_per_page)

    if next_page > total_pages:
        raise HTTPException(status_code=400, detail="Page out of range.")

    # Extract the requested page
    start_index = (next_page - 1) * lines_per_page
    end_index = start_index + lines_per_page
    page_content = all_lines[start_index:end_index]

    return {
        "current_page": next_page,
        "lines_per_page": lines_per_page,
        "total_pages": total_pages,
        "content": page_content
    }


@app.get("/less")
async def less_api(
    file_path: str,
    user_id: int,
    next_page: int = Query(1, ge=1)  # Default to first page, must be >= 1
):
    """
    Paginate file content for the `less` command.

    Args:
        file_path (str): The path of the file.
        user_id (int): The ID of the user requesting the file.
        next_page (int): The page number to display (default is 1).
    
    Returns:
        JSON response with the requested page and metadata.
    """
    lines_per_page = 10  # Default number of lines per page

    # Fetch the file record
    file_record = next(
        (f for f in fsDB.readData("files")["data"] if f["path"] == file_path and f["user_id"] == user_id), 
        None
    )
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found or access denied.")

    # Check read permissions
    if file_record.get("owner_read_permission") != True:
        raise HTTPException(status_code=403, detail=f"less: {file_record['name']}: Permission denied")

    # Fetch file content
    file_content = [
        chunk["chunk"].decode("utf-8") 
        for chunk in fsDB.readFileData("file_contents", file_record["file_id"])["data"]
    ]
    all_lines = "\n".join(file_content).splitlines()

    # Calculate total pages and validate next_page
    total_lines = len(all_lines)
    total_pages = math.ceil(total_lines / lines_per_page)

    if next_page > total_pages:
        raise HTTPException(status_code=400, detail="Page out of range.")

    # Extract the requested page
    start_index = (next_page - 1) * lines_per_page
    end_index = start_index + lines_per_page
    page_content = all_lines[start_index:end_index]

    return {
        "current_page": next_page,
        "lines_per_page": lines_per_page,
        "total_pages": total_pages,
        "content": page_content
    }


@app.get("/sort")
async def sort_file(
    file_path: str = None,
    user_id: int = None,
    numeric: bool = False,
    reverse: bool = False,
    case_insensitive: bool = False,
    unique: bool = False,
):
    """
    Sort the contents of a file or piped input based on specified flags.

    Args:
    - file_path (str): Path to the file to be sorted.
    - user_id (int): ID of the user accessing the file.
    - numeric (bool): Sort numerically if True.
    - reverse (bool): Sort in reverse order if True.
    - case_insensitive (bool): Ignore case when sorting if True.
    - unique (bool): Remove duplicate lines if True.
    - piped_input (str): Input data from a piped command.

    Returns:
    - JSON: Sorted content.
    """
    # Simulate fetching file data (replace with actual file retrieval logic)
    if file_path:
        file_record = next(
            (f for f in fsDB.readData("files")["data"] if f["path"] == file_path and f["user_id"] == user_id),
            None
        )
        if not file_record:
            raise HTTPException(status_code=404, detail="File not found or access denied.")
        
        file_chunks = fsDB.readFileData("file_contents", file_record["file_id"])["data"]
        content = "".join(chunk["chunk"].decode("utf-8") for chunk in file_chunks).splitlines()
    
    else:
        raise HTTPException(status_code=400, detail="Either `file_path` or `piped_input` must be provided.")

    # Apply sorting logic
    try:
        if case_insensitive:
            key_func = str.lower
        elif numeric:
            key_func = lambda x: float(re.search(r"\d+", x).group()) if re.search(r"\d+", x) else float('inf')
        else:
            key_func = None

        sorted_content = sorted(content, key=key_func, reverse=reverse)

        if unique:
            sorted_content = list(dict.fromkeys(sorted_content))  # Remove duplicates

        return {"content": sorted_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


### 10. **File Permissions**
def parse_numeric_permissions(numeric_permissions: str):
    """Convert numeric permissions (e.g., 755) to a dictionary of binary flags."""
    binary_permissions = [bin(int(digit))[2:].zfill(3) for digit in numeric_permissions]
    owner, group, others = binary_permissions
    return {
        "owner_read_permission": int(owner[0]),
        "owner_write_permission": int(owner[1]),
        "owner_execute_permission": int(owner[2]),
        "group_read_permission": int(group[0]),
        "group_write_permission": int(group[1]),
        "group_execute_permission": int(group[2]),
        "others_read_permission": int(others[0]),
        "others_write_permission": int(others[1]),
        "others_execute_permission": int(others[2]),
    }

def apply_symbolic_permissions(file_record, mode, permissions, user_type=None):
    """Apply symbolic permissions to a file record dictionary."""
    permission_map = {'r': 'read_permission', 'w': 'write_permission', 'x': 'execute_permission'}

    # Ensure the permissions string contains valid permission characters
    for perm in permissions:
        perm_field = permission_map.get(perm)
        if not perm_field:
            raise HTTPException(status_code=400, detail=f"Invalid symbolic permission '{perm}'.")

        # Determine which permission fields to update based on user type
        fields_to_update = []
        if user_type in ['u', None]:  # Owner
            fields_to_update.append(f"owner_{perm_field}")
        if user_type in ['g', None]:  # Group
            fields_to_update.append(f"group_{perm_field}")
        if user_type in ['o', None]:  # Others
            fields_to_update.append(f"others_{perm_field}")

        # Apply changes (set to 1 for '+' mode, set to 0 for '-' mode)
        for field in fields_to_update:
            file_record[field] = 1 if mode == '+' else 0


@app.post("/chmod")
async def chmod_path(file_path: str, user_id: int, permissions: str):
    """
    Updates the permissions for a file or directory.

    Parameters:
    - file_path (str): Path of the file or directory.
    - user_id (int): ID of the user performing the operation.
    - permissions (str): Permissions in numeric (e.g., 755) or symbolic (e.g., u+w) format.
    """
    # Check if permissions are numeric (e.g., 755) or symbolic (e.g., +x, u+w)
    is_numeric = permissions.isdigit() and len(permissions) == 3

    try:
        # Step 1: Check if the path matches a file
        file_record = next(
            (f for f in fsDB.readData("files")["data"] if f["path"] == file_path and f["user_id"] == user_id), None
        )
        table_name = "files"
        record_id_key = "file_id"

        # If not a file, check for a directory
        if not file_record:
            directory_record = next(
                (d for d in fsDB.readData("directories")["data"] if d["path"] == file_path and d["user_id"] == user_id),
                None
            )
            if not directory_record:
                raise HTTPException(status_code=404, detail="Path not found or access denied.")

            table_name = "directories"
            record_id_key = "dir_id"
            file_record = directory_record

        # Step 2: Handle numeric permissions
        if is_numeric:
            updated_permissions = parse_numeric_permissions(permissions)
            for key, value in updated_permissions.items():
                update_result = fsDB.updateData(table_name, key, value, record_id_key, file_record[record_id_key])
                if not update_result["success"]:
                    raise HTTPException(
                        status_code=500, detail=f"Failed to update {key} permission for the path."
                    )

        # Step 3: Handle symbolic permissions
        else:
            user_type = permissions[0] if permissions[0] in 'ugo' else None
            mode = permissions[1 if user_type else 0]
            perm_str = permissions[(2 if user_type else 1):]

            # Validate mode
            if mode not in ['+', '-']:
                raise HTTPException(status_code=400, detail="Invalid symbolic permission mode. Use '+' or '-'.")

            # Apply symbolic permissions
            apply_symbolic_permissions(file_record, mode, perm_str, user_type)

            # Update each modified permission in the database
            for key, value in file_record.items():
                if key.endswith('_permission'):
                    update_result = fsDB.updateData(table_name, key, value, record_id_key, file_record[record_id_key])
                    if not update_result["success"]:
                        raise HTTPException(
                            status_code=500, detail=f"Failed to update {key} permission for the path."
                        )

        # Update the modified_at timestamp
        modified_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fsDB.updateData(table_name, "modified_at", modified_at, record_id_key, file_record[record_id_key])

        return {"message": f"Permissions for '{file_path}' updated successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
    
"""
This main block gets run when you invoke this file. How do you invoke this file?

        python api.py 

After it is running, copy paste this into a browser: http://127.0.0.1:8080 

You should see your api's base route!

Note:
    Notice the first param below: api:app 
    The left side (api) is the name of this file (api.py without the extension)
    The right side (app) is the bearingiable name of the FastApi instance declared at the top of the file.
"""
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)
