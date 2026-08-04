import json
import traceback

from infrastructure.clients.llm_client import LLMClient
from infrastructure.clients.serapi_client import SerpApiClient

class DictionaryService:
    def __init__(self, llm_client: LLMClient, serapi_client: SerpApiClient):
        self.llm_client = llm_client
        self.serapi_client = serapi_client

    async def get_definition(self, word: str, tag: str, target_languages: list, language_detected: str):
        return await self.get_definition_from_serapi_search(word, tag, target_languages, language_detected)

    async def get_definition_from_serapi_search(self, word: str, tag: str, target_languages: list, language_detected: str):
        query = f'{word} meaning '
        try:
            definitions = await self.serapi_client.search(query)
            print(f"Target languages: {target_languages}")
            return await self.process_definitions(word, tag, definitions, target_languages, language_detected)
        except Exception as e:
            print("SerAPI search error:", repr(e))
            traceback.print_exc()
        return None

    async def process_definitions(self, word: str, tag: str, definitions, target_languages: list, language_detected: str):
        clean_write = f"""Clean and rewrite a definition for the word '{word}' as '{tag}' base on these definitions
                        {definitions}. """
        new_definitions = f"""Write definition for the word  '{word}' as '{tag}' """
        definitions_default = new_definitions if definitions == None else clean_write
        prompt = f""" {definitions_default}. Everything must be in {language_detected}, 
        in synonyms field add synonyms for this {word} 
        Add translations of the word in just those {len(target_languages)} languages {target_languages}. 
        Use the codes to identify the languages in translation field.
        filter the definitions you consider most appropiates and important and all 
        of the information must be compact in definition field in the json
        DO NOT use markdown.
        DO NOT use ```json
        DO NOT use ' to enclose the keys or values in the json
        Return a JSON object like:
        {{
          "synonyms": ["..", "..", ".."],
          "translation": [
            "en": ["..", "..", ".."],
            "pt": ["..", "..", ".."]
          ],
          "definition": "..."
        }}
        """
        response = await self.llm_client.complete(prompt)
        return json.loads(response)