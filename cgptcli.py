#!/usr/bin/env python3

# https://platform.openai.com/docs/guides/chat
# https://platform.openai.com/docs/api-reference/chat/create

import src.utils as utils
import openai
import json
import argparse
import os
import readline
from datetime import datetime

ITALIC = '\033[3m'
GREEN = '\033[32m'
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
max_tokens = 4000

historyFilePath = ''
firstMessage = ''
messages = []

def chat_with_gpt(prompt):
    global firstMessage
    global messages
    global historyFilePath

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
    if historyFilePath:
        filePath = 'chathistory/' + historyFilePath
    else:
        path = 'chathistory/' + datetime.now().strftime("%Y_%m_%d")
        dirExist = os.path.exists(path)
        if not dirExist:
            os.makedirs(path)

        firstMessageFormatted = firstMessage[0:35]
        firstMessageFormatted = ''.join(e for e in firstMessageFormatted if e.isalnum())
        firstMessageFormatted = firstMessageFormatted.replace("å", "a")
        firstMessageFormatted = firstMessageFormatted.replace("ä", "a")
        firstMessageFormatted = firstMessageFormatted.replace("ö", "o")

        filePath = path + '/' + firstMessageFormatted + '_' + datetime.now().strftime("%HH%MM%SS") + '.json' 
        historyFilePath = filePath.replace("chathistory/", "")

    with open(filePath, 'w') as outfile:
        outfile.write(json.dumps(messages))
    #############################

    return response.choices[0].message['content']

def readHistory(file):
    global messages
    global historyFilePath

    historyFilePath = file

    f = open('chathistory/' + file)
    data = json.load(f)
    messages = data
    print("\n")
    print(messages)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="The prompt to generate text from", nargs='?')
    parser.add_argument('-f', '--file') 

    args = parser.parse_args()
    prompt=args.prompt
    file=args.file

    if file:
        if prompt:
            print("ERROR no prompt when loading history file")
            exit()

        readHistory(file)

    print(GRAY + f"Model engine: {model}" + ENDC)
    print(GRAY + f"Max tokens: {max_tokens}" + ENDC)
    print("\nCHAT STARTED!\n")

    if prompt:
        response = chat_with_gpt(prompt)
        print(BLUE + "AI" + ENDC + f": {utils.getFormattedResponseText(response)}\n")

    while True:
        prompt = input(YELLOW + "You" + ENDC + ": ")
        
        #prompt = "Name two colors"

        response = chat_with_gpt(prompt)
        print(BLUE + "AI" + ENDC + f": {utils.getFormattedResponseText(response)}\n")

if __name__ == "__main__":
    main()
