from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

SYSTEM_PROMPT ="""
You are Hitesh Sir.You are a tech educator.You are a coding teacher 
"""

def persona(user_input):
    messages = [
        {"role" : "system" , "content" : SYSTEM_PROMPT},
        {"role" : "user" , "content" : user_input}
    ]
    result = client.chat.completions.create(
        model='gpt-4'
        messages=messages
        temperature=1.2
    )
    
