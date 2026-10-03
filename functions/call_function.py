import json
from openai.types.chat import ChatCompletionMessageToolCallUnion
from collections.abc import Callable
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(tool_call: ChatCompletionMessageToolCallUnion, verbose: bool = False):
    name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments or "{}")
    id = tool_call.id

    if verbose:
        print(f"Calling function - {name}({arguments})")
    else:
        print(f"Calling function - {name}")

    if not function_map[name]:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {name}",
        }

    # If function was found, we need to call it

    arguments["working_directory"] = "calculator"

    func = function_map[name]
    result = func(**arguments)

    return {"role": "tool", "tool_call_id": tool_call.id, "content": result}
