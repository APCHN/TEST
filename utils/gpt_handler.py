import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]
