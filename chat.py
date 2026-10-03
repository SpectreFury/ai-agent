import os
from dotenv import load_dotenv

from collections.abc import Iterable

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv();

MODEL = os.getenv("MODEL")

if not MODEL:
    raise RuntimeError("MODEL was not found")

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]


def generate_content(client: OpenAI, messages: Iterable[ChatCompletionMessageParam]):
    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=available_functions
    )

    return response
