import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

llm = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate(prompt):
    response = llm.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL_NAME"),
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    result = response.choices[0].message.content
    print(result)
    return result
