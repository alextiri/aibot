from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

print(get_file_content({'file_path': 'main.py'}))