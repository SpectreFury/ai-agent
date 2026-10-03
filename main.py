import os
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from chat import generate_content
from prompts import SYSTEM_PROMPT
from functions.call_function import call_function

load_dotenv()

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
user_prompt = str(args.user_prompt)
verbose = args.verbose

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY was not found!")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=API_KEY)

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": user_prompt},
]

for _ in range(20):
    response = generate_content(client, messages)

    if not response.usage:
        raise RuntimeError("Request failed")

    if verbose:
        print(f"User prompt: {user_prompt}")
        print("Prompt token: ", response.usage.prompt_tokens)
        print("Completion token: ", response.usage.completion_tokens)

    message = response.choices[0].message

    messages.append(message)

    if not message.tool_calls:
        print(message.content)
        break

    for tool_call in message.tool_calls:
        result = call_function(tool_call, verbose)
        messages.append(result)

        if verbose:
            print(f"-> {result["content"]}")
