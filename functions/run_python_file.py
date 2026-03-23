import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file and returns its output. The file must be located within the working directory or its subdirectories. Optionally, a list of arguments can be provided to the Python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of string arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Prevent running files outside working_directory
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Must exist and be a regular file
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        # Must be a Python file
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command
        command = ["python", target_file]
        if args:
            command.extend(args)

        # Run subprocess and capture output
        result = subprocess.run(
            command, 
            cwd=working_dir_abs, # Set the working directory properly.
            capture_output=True, # Capture output (i.e., stdout and stderr).
            text=True, # Decode the output to strings, rather than bytes
            timeout=30 # Set a timeout of 30 seconds to prevent infinite execution.
        )

        # Build an output string 
        output_string = ""

        if result.returncode != 0:
            output_string += f'Process exited with code {result.returncode}\n'

        if not result.stdout and not result.stderr:
            output_string += "No output produced"
        else:
            if result.stdout:
                output_string += f'STDOUT:\n{result.stdout}\n'
            if result.stderr:
                output_string += f'STDERR:\n{result.stderr}\n'

        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"