import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def suggest_code_improvements(code_snippet):
    prompt = f"Review the following code and suggest improvements:\n\n{code_snippet}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use gpt-3.5-turbo instead of gpt-4
        messages=[
            {"role": "system", "content": "You are a helpful code review assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']