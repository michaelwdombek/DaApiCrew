from langchain_community.tools import tool
from os import path



WORKING_DIR = "./workdir"


def _build_file_path(file_name: str, custom_dir: str = "") -> str:
    """Builds a file path from the file name and the custom directory"""
    if custom_dir != "":
        # remove the first  and last "/" if it exists
        custom_dir = custom_dir.strip("/")
        file_path = f"{WORKING_DIR}/{custom_dir}/{file_name}"
    else:
        file_path = f"{WORKING_DIR}/{file_name}"
    return file_path
# TODO: look at reading larger files in chunks
@tool("open a file and read it")
def read_file(file_name: str, custom_dir: str = "") -> str:
    """Useful for when you need to load content from a file on the filesystem.
    The input should be a file path as a string."""
    file_path = _build_file_path(file_name, custom_dir)
    with open(file_path) as file:
        return file.read()


@tool("write to a file")
def write_file(file_name_content: str, custom_dir: str = "") -> str:
    """writes the content into the filename provided
    inputs are the filename|content
    ie
    'test.txt'|+|'this is a test' will create a file called test.txt with the content 'this is a test'
    'app.py'|+|'print("hello world")' will create a file called app.py with the content 'print("hello world")'
    return the filename if the file was created successfully, else a error message
    """
    file_name, content = file_name_content.split("|+|")
    file_path = _build_file_path(file_name, custom_dir)
    with open(file_path, "w") as file:
        file.write(content)
    return file_name if path.exists(file_path) else f"Error creating file {file_name}"
