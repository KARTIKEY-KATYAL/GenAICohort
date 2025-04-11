from dotenv import load_dotenv
from openai import OpenAI
import os ,json
from collections import Counter

load_dotenv()

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

user_query = input("> ")

SYSTEM_PROMPT = """
You are a reasoning assistant. You solve problems by thinking through multiple different paths and then return your final conclusion based on what the majority of reasoning paths suggest.

Follow these steps:
1. Read the user question carefully.
2. Think step-by-step to solve it.
3. Generate different possible reasoning paths (be creative, but accurate).
4. Do not repeat exact same steps – vary structure slightly for diversity.
5. At the end, only return the answer, not the explanation.

Repeat this process multiple times to allow for self-consistency voting.
"""

def get_valid_responses(user_query,num_paths = 7):
    messages = [ 
        {"role" : "system" , "content" : SYSTEM_PROMPT},
        {"role" : "user" , "content" : user_query}    
    ]

    answers = []
    
    for _ in range(num_paths):
        result = client.chat.completions.create(
            model='gpt-4',
            temperature=1.2,
            messages = messages
        )
        answer = result.choices[0].message.content.strip()
        answers.append(answer)
        
    return answers  
    

def get_best_response(answers):
    counts = Counter(answers)
    most_common = counts.most_common(1)[0]
    return {
        "final_answer": most_common[0],
        "confidence": most_common[1] / len(answers),        
        "all_answers": answers
    }

responses = get_valid_responses(user_query,10)

best_response = get_best_response(responses)

print(best_response)