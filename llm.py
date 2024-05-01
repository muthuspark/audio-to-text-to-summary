from dotenv import dotenv_values
import requests
import json

config = dotenv_values(".env")


def chat_with_llama(message):
    url = "http://localhost:11434/api/generate"

    payload = json.dumps({
        "model": "llama3",
        "prompt": message,
        "stream": False
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['response'].strip()
