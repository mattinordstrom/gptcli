#!/usr/bin/env python3

import openai
import argparse

# Load API key from secret file
with open("secret", "r") as f:
    api_key = f.read().strip()

# Set API key
openai.api_key = api_key

# Set OpenAI model and parameters
model_engine = "text-davinci-003"
max_tokens = 256

def generate_text(prompt):
    # Generate text from the given prompt
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens
    )

    return response.choices[0].text

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="The prompt to generate text from")
    args = parser.parse_args()

    print(f"\033[90mModel engine: {model_engine}\033[0m")
    print(f"\033[90mMax tokens: {max_tokens}\033[0m")

    # Generate text from prompt
    text = generate_text(args.prompt)

    # Print generated text
    print(text)
