from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def get_llm_response(prompt: str) -> str:
    return client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    ).output_text