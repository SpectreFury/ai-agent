import os
from dotenv import load_dotenv

from collections.abc import Iterable

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

_ = load_dotenv();

MODEL = os.getenv("MODEL")
API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("BASE_URL")

if not MODEL:
    raise RuntimeError("MODEL was not found!")

if not API_KEY:
    raise RuntimeError("LLM_API_KEY was not found!")

if not BASE_URL:
    raise RuntimeError("BAE_URL was not found!")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]


def generate_content(messages: Iterable[ChatCompletionMessageParam]):
    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=available_functions
    )

    return response
