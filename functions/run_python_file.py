import os
import subprocess
from google import genai
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified Python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the desired Python file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Any arguments to be used when the Python file is run",
            ),            
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if not valid_target_file:
        return f'    Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'    Error: "{file_path}" does not exist or is not a regular file'
    
    if not target_file[-3:] == ".py":
        return f'    Error: "{file_path}" is not a Python file'
    
    command = ["python", target_file]

    if args:
        for arg in args:
            command.extend(arg)

    try:
        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        return_message = ""

        if result.returncode != 0:
            return_message += f"    Process exited with code {result.returncode}\n"
    
        if result.stdout == "":
            return_message += f"    No output produced\n"
        else:
            if error := result.stderr == "":
                error = "<None>"            
                
            return_message += f"    STDOUT: {result.stdout}\n    STDERR: {error}\n"

        return return_message
    
    except Exception as e:
        return f"    Error: executing Python file: {e}"

    