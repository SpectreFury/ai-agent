import os

def write_file(working_directory: str, file_path: str, content: str):
    try:
        abs_path = os.path.abspath(working_directory)

        abs_file_path = os.path.normpath(os.path.join(abs_path, file_path))
        is_valid_path = os.path.commonpath([abs_path, abs_file_path]) == abs_path

        if not is_valid_path:
            return (
                f"Cannot write to {file_path} as it is outside the permitted working directory"
            )

        # Return if it is a directory
        if os.path.isdir(abs_file_path):
            return f"Cannot write to {file_path} as it is a directory"

        os.makedirs(abs_path, exist_ok=True)
        with open(abs_file_path, "w", encoding="utf-8") as file:
            file.write(content)
            print(f"Successfully wrote to {file_path} {len(content)} characters written")

    except:
        return f"Error: some error occured"

print(write_file("calculator", "lorem.txt", "Hi"))
