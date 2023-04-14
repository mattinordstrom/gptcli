#!/usr/bin/env python3

import requests
import argparse
import json

# Load API key from secret file
with open("secret", "r") as f:
    api_key = f.read().strip()

# Set API endpoint and parameters
api_url = "https://api.openai.com/v1/images/generations"
size = "1024x1024"

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("prompt", help="The prompt to generate an image from")

args = parser.parse_args()
prompt = args.prompt
#prompt = "A red panda drinking coffee in a park"

print(f"\033[90mSize: {size}\033[0m")
print(" ")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Set request data
data = {
    "prompt": prompt,
    "size": size,
    "n": 1
}

# Send request to API
response = requests.post(api_url, headers=headers, data=json.dumps(data))

# Get image URL from response
image_url = response.json()["data"][0]["url"]

# Download image from URL and save to file
image_data = requests.get(image_url).content
with open("output.png", "wb") as f:
    f.write(image_data)

print(f"URL: {image_url}")
print(" ")
print("Saved locally as output.png!")