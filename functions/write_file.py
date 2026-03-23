import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file. The file must be located within the working directory or its subdirectories. If the file already exists, it will be overwritten. If the file does not exist, it will be created along with any necessary parent directories.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # If the file_path is outside the working_directory, return an error string.
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # If the file_path points to an existing directory (this is what os.path.isdir() checks for), return an error string.
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Make sure that all parent directories of the file_path exist. You can use os.makedirs() with the exist_ok=True argument to create any missing directories. If the necessary directory structure already exists, this will do nothing – which is what we want.
        parent = os.path.dirname(target_file)
        if parent:
            os.makedirs(parent, exist_ok=True)

        # Open the file at file_path in write mode ("w") and overwrite its contents with the content argument.
        with open(target_file, "w") as f:
            f.write(content)

        # If everything succeeds, return a string indicating that the write was successful.
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {e}'