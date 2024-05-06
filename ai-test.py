#! /usr/bin/env python3
import sys

from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=sys.argv[1],
)

inp = f"Can you make the title '{sys.argv[2]}' shorter and more spesific? If possible, mention it's size or dimentions, but do not mention quantity, what it is used for, or how it is used."

inp = f"What tags would you use to describe this product: '{sys.argv[2]}'"


chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": inp,
        }
    ],
    model="gpt-4",
)
print("Input: ", inp)
for choice in chat_completion.choices:
    print("Output: ", choice.message.content)
print("Tokens: ", chat_completion.usage.total_tokens, " ($0,09 / 1K tokens")
