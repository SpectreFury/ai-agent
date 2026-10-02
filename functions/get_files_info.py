import os


def get_files_info(working_directory: str, directory: str = "."):
    if not os.path.isdir(directory):
        return f"Error: {directory} is not a directory"

    abs_path = os.path.abspath(working_directory)

    target_dir = os.path.normpath(os.path.join(abs_path, directory))
    is_valid_path = os.path.commonpath([abs_path, target_dir]) == abs_path

    if not is_valid_path:
        return (
            f"Cannot list {directory} as it is outside thte permitted working directory"
        )


get_files_info("calculator")
