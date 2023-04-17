#!/usr/bin/env python3

# https://platform.openai.com/docs/guides/chat
# https://platform.openai.com/docs/api-reference/chat/create

import openai
import json
import argparse
import os
from datetime import datetime

ITALIC = '\033[3m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
GRAY = '\033[90m'
ENDC = '\033[0m'

# Load API key from secret file
with open("secret", "r") as f:
    api_key = f.read().strip()

# Set API key and chat model
openai.api_key = api_key
model = "gpt-3.5-turbo"
max_tokens = 2000

print(GRAY + f"Model engine: {model}" + ENDC)
print(GRAY + f"Max tokens: {max_tokens}" + ENDC)

firstMessage = ''
messages = []
def chat_with_gpt(prompt):
    global firstMessage
    if firstMessage == '':
        firstMessage = prompt

    messages.append({'role': 'user', 'content': prompt})

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )

    messages.append({'role': response.choices[0].message['role'], 'content': response.choices[0].message['content']})
    
    print(ITALIC + GRAY + f"Prompt tokens: {response.usage.prompt_tokens} | Compl. tokens: {response.usage.completion_tokens} | Tot. tokens: {response.usage.total_tokens} | Resp. model: {response.model}" + ENDC)

# Save history
###########################
    path = 'chathistory/' + datetime.now().strftime("%Y%m%d")
    dirExist = os.path.exists(path)
    if not dirExist:
        os.makedirs(path)

    firstMessageFormatted = firstMessage[0:40]
    firstMessageFormatted = ''.join(e for e in firstMessageFormatted if e.isalnum())
    firstMessageFormatted = firstMessageFormatted.replace("å", "a")
    firstMessageFormatted = firstMessageFormatted.replace("ä", "a")
    firstMessageFormatted = firstMessageFormatted.replace("ö", "o")
    with open(path + '/' + firstMessageFormatted + '.json', 'w') as outfile:
        outfile.write(json.dumps(messages))
#############################

    return response.choices[0].message['content']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="The prompt to generate text from", nargs='?')

    print("CHAT STARTED!\n")

    args = parser.parse_args()
    prompt=args.prompt

    if prompt:
        response = chat_with_gpt(prompt)
        print(BLUE + "AI" + ENDC + f": {response}\n")

    while True:
        prompt = input(YELLOW + "You" + ENDC + ": ")
        
        #prompt = "Name two colors"

        response = chat_with_gpt(prompt)
        print(BLUE + "AI" + ENDC + f": {response}\n")

if __name__ == "__main__":
    main()