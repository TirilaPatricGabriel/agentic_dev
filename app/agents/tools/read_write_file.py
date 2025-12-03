from langchain_core.tools import tool
import os

@tool
def read_file(file_path: str):
    """Reads content from a file."""
    if not os.path.exists(file_path):
        return f"Error: File {file_path} does not exist."
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool
def write_file(content: str, file_path: str):
    """Writes content to a file."""
    try:
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"