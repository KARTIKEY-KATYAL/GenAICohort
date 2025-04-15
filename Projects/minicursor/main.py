from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

SYSTEM_PROMPT="""
"""

# response = client.chat.completions.create()

response = client.chat.