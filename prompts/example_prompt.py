import json
import traceback

from infrastructure.clients.llm_client import LLMClient
from infrastructure.clients.serapi_client import SerpApiClient

class ExamplePromptBuilder:
    def __init__(self, llm_client: LLMClient, serapi_client: SerpApiClient):
        self.llm_client = llm_client
        self.serapi_client = serapi_client

    async def get_examples(self, word: str, tag: str, language_detected: str):
        return await self.get_examples_from_serapi_search(word, tag, language_detected)
    
    async def get_examples_from_serapi_search(self, word: str, tag: str, language_detected: str):
        query = f'{word} as {tag} examples in {language_detected}'
        try:
            examples = await self.serapi_client.search(query)
            return await self.process_examples(word, tag, examples, language_detected)
        except Exception as e:
            print("SerAPI search error:", repr(e))
            traceback.print_exc()
        return None

    async def process_examples(self, word,  tag: str, examples, language_detected):
        clean_write = f"""Clean and rewrite 3 examples of the word '{word}' as '{tag}' base on these examples
                        {examples}. """
        prompt = f""" {clean_write}. Everything must be in {language_detected}, 
        filter the examples you consider most appropiates and important and all 
        of the information must be compact in examples field in the json
        DO NOT use markdown.
        DO NOT use ```json
        Return a JSON object like:
        {{
          "examples": ["..", "..", ".."]
        }}
        """
        response = await self.llm_client.complete(prompt)
        return json.loads(response)