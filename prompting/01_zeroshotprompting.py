# 1. Zero-shot Prompting: The model is given a direct question or task without prior examples.

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

user_query = input("> ")

result = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "user", "content": user_query } # Zero Shot Prompting
    ]
)

print(result.choices[0].message.content)