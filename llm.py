import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from prompts import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(state, user_input):

    
    prompt = build_prompt(state, user_input)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    if content is None:
        raise ValueError("LLM returned no content")
    return content


def build_prompt(state, user_input):
    history = "\n".join([
        f"COMMAND: {h['command']}\nOUTPUT:\n{h['output']}\n"
        for h in state["history"][-3:]
    ])

    if not history:
        history = "No commands have been run yet."

    return f"""
User problem:
{user_input}

Recent investigation history:
{history}

Your task:
1. Analyse the current situation
2. Produce a short 3-step investigation plan
3. Propose the single best next command to run now
"""
