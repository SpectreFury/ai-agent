import os

MAX_CHARS = 10000


def get_file_content(working_directory: str, file_path: str):
    try:
        abs_path = os.path.abspath(working_directory)

        file_path = os.path.normpath(os.path.join(abs_path, file_path))
        is_valid_path = os.path.commonpath([abs_path, file_path]) == abs_path

        # If not valid path
        if not is_valid_path:
            return f"Cannot list {file_path} as it is outside the permitted working directory"

        # If not a file
        if not os.path.isfile(file_path):
            return f"Not a file"

        with open(file_path, "r", encoding="utf-8") as file:
            file_output = file.read(MAX_CHARS)
            print("Length: ", len(file_output))
            print("Content: ", file_output)

            if file.read(1):
                file_output += (
                    f"[...File {file_path} truncated at {MAX_CHARS} characters]"
                )

            return file_output
    except:
        return f"Error: some error occured"
