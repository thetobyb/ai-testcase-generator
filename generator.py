# generator.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_test_cases(user_input: str, context: str) -> str:
    prompt = f"""
You are a QA engineer. {context}

Input:
\"\"\"
{user_input}
\"\"\"

Generate test cases in this format:
- Title
- Type (Positive / Negative / Edge)
- Steps
- Expected Result
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
