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

    return f"""
    User problem:
    {user_input}

    Recent investigation:
    {history}

    What is the next best command?
    """

