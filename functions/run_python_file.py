from config import *
from google.genai import types
import os
import subprocess
import sys

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs python files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to the file to run, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="list of arguments to be provided to the python file",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    if os.path.abspath(full_path).startswith(os.path.abspath(working_directory)) == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(full_path) == False:
        return f'Error: File "{file_path}" not found.'
    if os.path.splitext(full_path)[1] != '.py':
        return f'Error:"{file_path}" is not a Python file.'
    else:
        try:
            completed_process = subprocess.run(
                [sys.executable, file_path, *args],
                cwd=working_directory,
                timeout=30,
                capture_output=True,
                text=True,
            )
            if completed_process.returncode != 0:
                return f"STDOUT:{completed_process.stdout}\nSTDERR:{completed_process.stderr}\nProcess exited with code {completed_process.returncode}"
            if completed_process.stdout == "" and completed_process.stderr == "":
                return f"No output produced."
            return f"STDOUT:{completed_process.stdout}\nSTDERR:{completed_process.stderr}"
        except Exception as e:
            return f"Error: executing Python file; {e}"
 
