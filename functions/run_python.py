import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        completed_process = subprocess.run(['python', file_path] + args, timeout=30, capture_output=True, cwd=working_directory)
        stdout = completed_process.stdout.decode()
        stderr = completed_process.stderr.decode()
        output = f'STDOUT: {stdout}\nSTDERR: {stderr}'
        if not stdout and not stderr:
            return "No output produced."
        if completed_process.returncode != 0:
            output += f"\nProcess exited with code {completed_process.returncode}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the given file, taking any optional arguments into consideration",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path from where to run the required file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The optional arguments that can be provided to the function",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Individual argument to be passed to the Python file"
                )
            )
        },
    ),
)