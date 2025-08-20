import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    if os.path.abspath(full_path).startswith(os.path.abspath(working_directory)) == False:
        return f'Error: cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(full_path) == False:
        return f'Error: "{directory}" is not a directory'
    else:
        output = []
        for x in os.listdir(full_path):
            output.append(f"- {x}: file_size={os.path.getsize(os.path.join(full_path,x))} bytes, is_dir={os.path.isdir(os.path.join(full_path,x))}")
        return "\n".join(output)

print(get_files_info("calculator", "."))
