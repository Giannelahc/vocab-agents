import json

from infrastructure.clients.llm_client import LLMClient

class PosTaggerPromptBuilder:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def getTag(self, word):
        return await self.process_word(word)

    async def process_word(self, word, languaje_detected):
        prompt = f"""
        Provide the grammar types 
        for example verb, noun, relative pronoun, preposition, adverb, expression and so on 
        for this '{languaje_detected}' '{word}'
        Rules:
        - Only include grammatical types that are truly used in real language.
        - If unsure, return only the most common type.
        - Do not invent meanings.
        All the types in english. Be specific to not lose information
        DO NOT use markdown.
        DO NOT use ```json
        Return a JSON object like:
        {{
          "types": ["verb", "noun"]
        }}
        """
        response = await self.llm_client.complete(prompt)
        return json.loads(response)