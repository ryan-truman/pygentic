from config import *
import os
import subprocess
import sys

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
                return f"Process exited with code {completed_process.returncode}"
            if completed_process.stdout == "":
                return f"No output produced."
            return f"STDOUT:{completed_process.stdout}\nSTDERR:{completed_process.stderr}"
        except Exception as e:
            return f"Error: executing Python file; {e}"
 
