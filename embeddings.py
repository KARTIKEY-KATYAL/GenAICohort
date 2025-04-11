from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

text = "The artificial intelligence revolution has transformed how we work, communicate, and solve complex problems in the modern digital era."

response = client.embeddings.create(
    input = text,
    model = 'text-embedding-3-small'
)

print("response API KEY",response.data[0].embedding)