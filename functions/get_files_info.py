from config import *
import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    if os.path.abspath(full_path).startswith(os.path.abspath(working_directory)) == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(full_path) == False:
        return f'Error: "{directory}" is not a directory'
    else:
        try:
            output = []
            for x in os.listdir(full_path):
                output.append(f"- {x}: file_size={os.path.getsize(os.path.join(full_path,x))} bytes, is_dir={os.path.isdir(os.path.join(full_path,x))}")
            return "\n".join(output)
        except exception as e:
            return f"Error:{e}"
