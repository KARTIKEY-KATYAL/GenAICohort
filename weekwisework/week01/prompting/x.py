import os
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from collections import Counter

load_dotenv()

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

# PROMPTS
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

MODI_PERSONA_PROMPT = """
You are Prime Minister Narendra Modi. You speak with a visionary tone, using patriotic and motivational language.
You answer thoughtfully, sometimes quoting Indian culture or your own speeches, but you remain grounded and direct.

When the user asks a question, respond with inspiration and national pride, while still addressing the core of the question.
End your message with a powerful closing line, like a slogan.

Stay in character throughout.
"""

ISRO_CHIEF_PROMPT = """
You are the Chief of ISRO, India’s space agency. Respond as a top scientist and mission leader.
Use technical language appropriately but stay accessible to the general public.
Describe processes or achievements with pride in India's advancements.

When asked a question, give insight like you're explaining it to the media or briefing the government.

Stay in role and use phrases like "At ISRO, we..." or "In our lunar program, we have achieved..."
"""

PROMPT_MAP = {
    "reasoning": SYSTEM_PROMPT,
    "modi": MODI_PERSONA_PROMPT,
    "isro": ISRO_CHIEF_PROMPT
}


def get_valid_responses(user_query, num_paths=7, prompt_type="reasoning"):
    prompt = PROMPT_MAP.get(prompt_type, SYSTEM_PROMPT)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_query}
    ]

    answers = []
    for _ in range(num_paths):
        result = client.chat.completions.create(
            model='gpt-4',
            temperature=1.2,
            messages=messages
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


def main():
    parser = argparse.ArgumentParser(description="Multimodal GPT Assistant with Prompt Modes")
    parser.add_argument("mode", choices=["reasoning", "modi", "isro"], help="Select the bot persona or reasoning style")
    parser.add_argument("--paths", type=int, default=7, help="Number of reasoning paths (for self-consistency)")
    args = parser.parse_args()

    user_query = input("> ")

    responses = get_valid_responses(user_query, args.paths, prompt_type=args.mode)
    best_response = get_best_response(responses)

    print("\n🎯 Final Answer:", best_response["final_answer"])
    print("📊 Confidence:", f"{best_response['confidence']*100:.1f}%")
    print("\n🧠 All Answers:")
    for i, ans in enumerate(best_response["all_answers"], 1):
        print(f"{i}. {ans}")


if __name__ == "__main__":
    main()
