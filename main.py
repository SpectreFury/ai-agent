import argparse
from dotenv import load_dotenv
from chat import generate_content
from prompts import SYSTEM_PROMPT
from functions.call_function import call_function

EXIT_CODES = set([":q", "exit"])

load_dotenv()

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
verbose = args.verbose

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

# Max 20 loops since we poor
for i in range(20):
    if not len(messages):
        break

    last_message = messages[-1]
    if last_message["role"] == "assistant" or last_message["role"] == "system":
        prompt = input("Query: ").strip()
        if not prompt:
            raise RuntimeError("No query")

        if prompt in EXIT_CODES:
            print("See ya")
            break

        messages.append({"role": "user", "content": prompt})

    response = generate_content(messages)

    if not response.usage:
        raise RuntimeError("Request failed")

    if verbose:
        print("User prompt: ", prompt)
        print("Prompt token: ", response.usage.prompt_tokens)
        print("Completion token: ", response.usage.completion_tokens)

    message = response.choices[0].message

    assistant_message = {"role": "assistant", "content": message.content}
    if message.tool_calls:
        assistant_message["tool_calls"] = [
            tc.model_dump(exclude_none=True) for tc in message.tool_calls
        ]
    messages.append(assistant_message)

    if not message.tool_calls:
        # Final response before new query
        print(message.content)
        continue

    for tool_call in message.tool_calls:
        result = call_function(tool_call, verbose)
        messages.append(result)

        if verbose:
            print(f"-> {result["content"]}")
