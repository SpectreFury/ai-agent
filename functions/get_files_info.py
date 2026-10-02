import os


def get_files_info(working_directory: str, directory: str = "."):
    try:
        if not os.path.isdir(directory):
            return f"Error: {directory} is not a directory"

        abs_path = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(abs_path, directory))
        is_valid_path = os.path.commonpath([abs_path, target_dir]) == abs_path

        if not is_valid_path:
            return (
                f"Cannot list {directory} as it is outside thte permitted working directory"
            )

        # Iterate over the files

        files = os.listdir(target_dir)
        res = ""

        for file in files:
            file_path = os.path.join(target_dir, file)
            res += f"- {file}, file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)} \n"

        return res

    except:
        return f"Error: some error occured"

