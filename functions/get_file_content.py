from config import *
import os
from google.genai import types

schema_get_file_content= types.FunctionDeclaration(
    name="get_file_content",
    description="returns the first 10000 characters of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read content from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

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
