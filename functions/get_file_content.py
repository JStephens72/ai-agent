import os
from config import MAX_CHARS
from google import genai
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the specified file relative to the working directory, providing the content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the desired file",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if not valid_target_file:
        return f'    Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'    Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file, "r") as file:
            contents = file.read(MAX_CHARS)
            if file.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    
    except FileNotFoundError:
        return f'    Error: "{file_path}" not found'
    
    except IOError:
        return f'    Error: IO error opening "{file_path}"'
          
    else:
        return contents
    

