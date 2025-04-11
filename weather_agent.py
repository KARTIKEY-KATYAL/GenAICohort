from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

result = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        { "role": "user", "content": "what is weather of Faridabad" } # Zero Shot Prompting
    ]
)

print(result.choices[0].message.content)