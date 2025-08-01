import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        abs_working_dir = os.path.abspath(working_directory)
        if not full_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        files = os.listdir(full_path)
        lines = []
        for file in files:
            file_path = os.path.join(full_path, file)
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            lines.append(f'- {file}: file_size={file_size} bytes, is_dir={is_dir}')
        output = '\n'.join(lines)
        return output
    except Exception as e:
        return f"Error: {str(e)}"

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