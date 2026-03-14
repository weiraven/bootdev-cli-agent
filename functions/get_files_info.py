import os

def get_files_info(working_directory, directory="."):
    """
    Get information about files in a specified directory.

    Args:
        working_directory (str): The base directory to search within.
        directory (str): The subdirectory to search for files. Defaults to the current directory.
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.commonpath([working_dir_abs, target_directory]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        lines = []

        for item in os.listdir(target_directory):
            item_path = os.path.join(target_directory, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return "\n".join(lines)

    except Exception as e:        
        return f"Error: {e}"


