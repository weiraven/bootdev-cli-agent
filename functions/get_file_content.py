import os
from config import MAX_CHARACTERS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file and returns it as a string. The file must be located within the working directory or its subdirectories. If the file is larger than 10,000 characters, only the first 10,000 characters will be returned, along with a note indicating that the content was truncated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path) -> str:
    try:   
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # If the file_path is outside the working_directory, return the error string below. To validate the path, you can use essentially the same logic that you wrote for get_files_info.
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # If the file_path is not a file, again, return an error string
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read the file and return its contents as a string. Read only up to 10000 characters from the file, in case it's very large.
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARACTERS)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'

        return content
    
    except Exception as e:
        return f'Error: {e}'
    
    
