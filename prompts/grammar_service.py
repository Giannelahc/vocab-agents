import json
from textwrap import dedent

from infrastructure.clients.llm_client import LLMClient

class GrammarService:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client


    async def get_gender(self, word, tag, target_language):
        prompt = dedent(f"""
        '{word}' as a {tag} in {target_language} is masculine or feminine
        If it does not have a gender, just use 'ND'
        DO NOT use markdown.
        DO NOT use ```json
        Return a JSON object like:
        {{
            "gender": ".."
        }}
        """)
        response_text = await self.llm_client.complete(prompt)
        response = json.loads(response_text.strip())
        return response
    
    async def get_conjugation(self, word, target_language):
        prompt = dedent(f"""
        Provide the conjugation for present tense, past participle and future tense used for this '{word}' in {target_language},
        for the first singular person and for first and third person in plural if they have variations,
        if not, just specify the conjugation for the first singular person.
        DO NOT use markdown.
        DO NOT use ```json
        Return a JSON object like:
        {{
            "conjugation": {{
                "present": ["..", "..", ".."],
                "past_participle": ["..", "..", ".."],
                "future": ["..", "..", ".."]
            }}
        }}
        """)
        response_text = await self.llm_client.complete(prompt)
        response = json.loads(response_text.strip())
        return response

