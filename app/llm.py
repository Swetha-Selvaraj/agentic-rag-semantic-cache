from transformers import pipeline
import os
import dotenv
dotenv.load_dotenv()

from openai import AzureOpenAI
llm = AzureOpenAI(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"))

def generate(prompt):
    response = llm.chat.completions.create(
        model="gpt-5-chat",
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=300
    )
    result = response.choices[0].message.content
    print(result)
    return result