import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()
user_prompt = args.user_prompt

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY was not found!")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=API_KEY)

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[{"role": "user", "content": user_prompt}],
)

if not response.usage:
    raise RuntimeError("Request failed")

print("Prompt token: ", response.usage.prompt_tokens)
print("Prompt token: ", response.usage.completion_tokens)
print(response.choices[0].message.content)
