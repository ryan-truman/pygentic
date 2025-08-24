from config import *
import os

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    if os.path.abspath(full_path).startswith(os.path.abspath(working_directory)) == False:
        return f'Error: Cannot read "{full_path}" as it is outside the permitted working directory'
    if os.path.isfile(full_path) == False:
        return f'Error: File not found or is not a regular file: "{full_path}"'
    else:
        try:
            with open(full_path, "r") as f:
                file_content = f.read(MAX_CHARS)
                if len(file_content) == 10000:
                    return f'{file_content}...File "{file_path}" truncated at 10000 characters'
                else:
                    return file_content
        except Exception as e:
            return f"Error:{e}"
