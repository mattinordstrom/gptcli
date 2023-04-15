#!/usr/bin/env python3

# https://platform.openai.com/docs/guides/chat
# https://platform.openai.com/docs/api-reference/chat/create

import openai
import sys
import argparse

# Load API key from secret file
with open("secret", "r") as f:
    api_key = f.read().strip()

# Set API key and chat model
openai.api_key = api_key
model = "gpt-3.5-turbo"
max_tokens = 500

print(f"\033[90mModel engine: {model}\033[0m")
print(f"\033[90mMax tokens: {max_tokens}\033[0m")

messages = []
def chat_with_gpt(prompt):
    messages.append({'role': 'user', 'content': prompt})

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )

    messages.append({'role': 'system', 'content': response.choices[0].message['content']})
    
    print(f"\033[90mPrompt tokens: {response.usage.prompt_tokens} | Compl. tokens: {response.usage.completion_tokens} | Tot. tokens: {response.usage.total_tokens} | Resp. model: {response.model}\033[0m")

    return response.choices[0].message['content']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="The prompt to generate text from", nargs='?')

    print("Type 'quit' to exit at any time.\n")

    args = parser.parse_args()
    prompt=args.prompt

    if prompt:
        response = chat_with_gpt(prompt)
        print(f"\033[34mAI\033[0m: {response}\n")

    while True:
        prompt = input("\033[33mYou\033[0m: ")
        #prompt = "Name two colors"

        if prompt.lower() == "quit":
            print("Goodbye!")
            sys.exit()

        response = chat_with_gpt(prompt)
        print(f"\033[34mAI\033[0m: {response}\n")

if __name__ == "__main__":
    main()