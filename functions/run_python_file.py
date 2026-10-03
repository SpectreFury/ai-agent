import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute a python file given the file path and optional argument in a working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the python file that is to be run in a given working directory",
                },
                "args": {
                    "type": "list[string]",
                    "description": "Optional list of arguments to execute the file with in a given working directory (default is None).",
                },
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
):
    try:
        abs_path = os.path.abspath(working_directory)

        abs_file_path = os.path.normpath(os.path.join(abs_path, file_path))
        is_valid_path = os.path.commonpath([abs_path, abs_file_path]) == abs_path

        if not is_valid_path:
            return (
                f"Cannot write to {file_path} as it is outside the permitted working directory"
            )

        # Return if it is a directory
        if not os.path.isfile(abs_file_path):
            return f"Cannot execute to {file_path} as it is not a file"

        # Check if file is a python file
        if not abs_file_path.endswith(".py"):
            return f"Not a python file"

        command = ["python", abs_file_path]
        if args and len(args):
            command.extend(args)

        result = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return f"Processed exited with with code {result.returncode}"

        if not result.stderr and not result.stdout:
            return "No output produced"

        return f"STDOUT: {result.stdout} \n STDERR: {result.stderr}"

    except:
        return f"Got some error"
