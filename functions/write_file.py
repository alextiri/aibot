import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(os.path.dirname(abs_file_path)):
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
    with open(abs_file_path, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites the file at the given path with the provided content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path from where to access the file that needs to be written over",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content of the accessed file"
            )
        },
    ),
)