from collections.abc import Iterable

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


def generate_content(client: OpenAI, messages: Iterable[ChatCompletionMessageParam]):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    return response
